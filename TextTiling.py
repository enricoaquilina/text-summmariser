from collections import Counter
from math import sqrt
import numpy as np
import re
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords

lemmatizer = WordNetLemmatizer()
stop_words = stopwords.words('english')


class TextTiling:

    def __init__(self):
        print("TextTiling: Segmenting textual data")

    def tokenize_string(self, input_string, w):
        tokens = []
        paragraph_breaks = []
        token_count = 0
        token_sequences = []
        index = 0
        count = Counter()

        paragraphs = [s.strip() for s in input_string.splitlines() if s != ""]
        pattern = r"((?:[a-z]+(?:[-'][a-z]+)*))"

        for paragraph in paragraphs:
            paragraph_tokens = re.findall(pattern, paragraph)
            tokens.extend(paragraph_tokens)
            token_count += len(paragraph_tokens)
            paragraph_breaks.append(token_count)

        paragraph_breaks = paragraph_breaks[:-1]

        for i in range(len(tokens)):
            count[tokens[i]] += 1
            index += 1
            if index % w == 0:
                token_sequences.append(count)
                count = Counter()
                index = 0

        for i in range(len(tokens)):
            count[tokens[i]] += 1
            index += 1
            if index % w == 0:
                token_sequences.append(count)
                count = Counter()
                index = 0

        # remove stop words from each sequence
        for i in range(len(token_sequences)):
            token_sequences[i] = [lemmatizer.lemmatize(word) for word in token_sequences[i] if word not in stop_words]

        # lemmatize the words in each sequence
        for i in range(len(token_sequences)):
            token_sequences[i] = [lemmatizer.lemmatize(word) for word in token_sequences[i]]

        unique_tokens = [word for word in set(tokens) if word not in stop_words]

        return (token_sequences, unique_tokens, paragraph_tokens)

    # compute lexical score for the gap between pairs of text sequences.
    # it starts assigning scores after the first sequence
    def vocab_introduction(self, token_sequences, w):
        new_words1 = set()
        new_words2 = set(token_sequences[0])

        scores = []
        w2 = w * 2

        for i in range(1, len(token_sequences) - 1):
            # words to the left of the gap
            new_words_1 = set(token_sequences[i - 1]).difference(new_words1)
            new_words_2 = set(token_sequences[i + 1]).difference(new_words2)

            # calculate the score and update score array
            scores.append(((len(new_words_1) + len(new_words_2)) / w2))

            new_words1 = new_words1.union(token_sequences[i - 1])
            new_words2 = new_words2.union(token_sequences[i + 1])

        b1 = len(set(token_sequences[len(token_sequences) - 1]).difference(new_words1))
        scores.append(b1 / w2)
        return scores

    # computes similarity scores for adjacent blocks of token sequences
    def block_score(self, k, token_sequence, unique_tokens):
        score_block = []
        before_count = Counter()
        after_count = Counter()

        # calculate score for each gap with at least k tokens on each side
        for gap_index in range(1, len(token_sequence)):
            current_k = min(gap_index, k, len(token_sequence) - gap_index)
            before_block = token_sequence[gap_index - current_k: gap_index]
            after_block = token_sequence[gap_index: gap_index + current_k]

            for i in range(current_k):
                before_count = before_count + Counter(token_sequence[gap_index + i - current_k])
                after_count = after_count + Counter(token_sequence[gap_index + i])

            # calculate and store score
            numerator = 0.0
            before_sum = 0.0
            after_sum = 0.0

            for token in unique_tokens:
                numerator = numerator + (before_count[token] * after_count[token])
                before_sum = before_sum + (before_count[token] ** 2)
                after_sum = after_sum + (after_count[token] ** 2)

            denominator = sqrt(before_sum * after_sum)

            if denominator == 0:
                denominator = 1

            score_block.append(numerator / denominator)

        return score_block

    # computes cutoff for depth scores above which gaps are considered boundaries
    def get_depth_cutoff(self, lex_scores, liberal=True):
        mean = np.mean(lex_scores)
        stdev = np.std(lex_scores)
        return mean - stdev if liberal else mean - stdev / 2

    # computes depth score for the specified side of the specified gap
    def get_depth_side_score(self, lex_scores, current_gap, left):
        depth_score = 0
        i = current_gap

        while lex_scores[i] - lex_scores[current_gap] >= depth_score:
            depth_score = lex_scores[i] - lex_scores[current_gap]
            i = i - 1 if left else i + 1
            if (i < 0 and left) or (i == len(lex_scores) and not left):
                break
        return depth_score

    # get the gaps to be considered as boundaries based on gap lexical scores
    def get_gap_boundaries(self, lex_scores):
        boundaries = []
        cutoff = self.get_depth_cutoff(lex_scores)

        for i, score in enumerate(lex_scores):
            depth_left_score = self.get_depth_side_score(lex_scores, i, True)
            depth_right_score = self.get_depth_side_score(lex_scores, i, False)

            depth_score = depth_left_score + depth_right_score
            if depth_score >= cutoff:
                boundaries.append(i)
        return boundaries

    # get location of paragraphs where subtopic boundaries occur
    def get_boundaries(self, lex_scores, p_locs, w):
        par_boundaries = set()

        gap_boundaries = self.get_gap_boundaries(lex_scores)
        token_boundaries = [w * (gap + 1) for gap in gap_boundaries]

        for i in range(len(token_boundaries)):
            par_boundaries.add(min(p_locs, key=lambda b: abs(b - token_boundaries[i])))

        return sorted(list(par_boundaries))

    # get texttiles in the input text based on paragraph locations and boundaries
    def segment_text(self, boundaries, p_locs, input_text):
        text_tiles = []
        paragraphs = [s.strip() for s in input_text.splitlines()]

        paragraphs = [s for s in paragraphs if s != ""]
        split_indices = [p_locs.index(b) + 1 for b in boundaries]

        start_index = 0

        for i in split_indices:
            text_tiles.append(paragraphs[start_index:i])
            start_index = i
        text_tiles.append(paragraphs[start_index:])

        output = []

        for i, tile in enumerate(text_tiles):
            out_string = ''
            for paragraph in tile:
                out_string += ' '
                out_string += paragraph
            output.append(out_string)

        return output
