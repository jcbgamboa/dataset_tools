import spacy

import matplotlib.pyplot as plt
import numpy as np

#from prettytable import PrettyTable
import pandas as pd

target_words = [
    # Positive words
    'love',
    'great',
    'good',
    'wonderful',
    'awesome',

    # Negative words
    'hate',
    'horrible',
    'bad',
    'terrible',
    'awful'
]

other_words = [
    # All words found in "talkenglish.com/vocabulary"
    # Since they give a frequency, I am taking all words with frequency at
    # least 15.

    # Nouns
    'science',
    'library',
    'nature',
    'fact',
    'product',
    'idea',
    'temperature',
    'investment',
    'area',
    'society',
    'activity',
    'story',
    'industry',
    'media',
    'thing',
    'oven',
    'community',
    'definition',
    'safety',
    'quality',
    'development',
    'language',
    'management',
    'player',
    'variety',
    'video',
    'week',
    'security',
    'country',
    'exam',
    'movie',
    'organization',
    'equipment',
    'physics',
    'analysis',
    'policy',
    'series',
    'thought',
    'basis',
    'boyfriend',
    'direction',
    'strategy',
    'technology',
    'army',
    'camera',
    'freedom',
    'paper',
    'environment',
    'child',
    'instance',
    'month',
    'truth',
    'marketing',
    'university',
    'writing',
    'article',
    'department',
    'difference',
    'goal',
    'news',
    'audience',
    'fishing',
    'growth',
    'income',
    'marriage',
    'user',
    'combination',
    'failure',
    'meaning',
    'medicine',
    'philosophy',
    'teacher',
    'communication',
    'night',
    'chemistry',
    'disease',
    'disk',
    'energy',
    'nation',
    'road',
    'role',
    'soup',
    'advertising',
    'location',
    'success',
    'addition',
    'apartment',
    'education',
    'math',
    'moment',
    'painting',
    'politics',
    'attention',
    'decision',
    'event',
    'property',
    'shopping',
    'student',
    'wood',
    'competition',
    'distribution',
    'entertainment',
    'office',
    'population',
    'president',
    'unit',
    'category',
    'cigarette',
    'context',
    'introduction',
    'opportunity',
    'performance',
    'driver',
    'flight',
    'length',
    'magazine',
    'newspaper',
    'relationship',
    'teaching',
    'cell',
    'dealer',
    'finding',
    'lake',
    'member',
    'message',
    'phone',
    'scene',
    'appearance',
    'association',
    'concept',
    'customer',
    'death',
    'discussion',
    'housing',
    'inflation',
    'insurance',
    'mood',
    'woman',

    # Verbs
    'is',
    'are',
    'has',
    'get',
    'see',
    'need',
    'know',
    'would',
    'find',
    'take',
    'want',
    'does',
    'learn',
    'become',
    'come',
    'include',
    'thank',
    'provide',
    'create',
    'add',
    'understand',
    'consider',
    'choose',
    'develop',
    'remember',
    'determine',
    'grow',
    'allow',
    'supply',
    'bring',
    'improve',
    'maintain',
    'begin',
    'exist',
    'tend',
    'enjoy',
    'perform',
    'decide',
    'identify',
    'continue',
    'protect',
    'require',
    'occur',
    'write',
    'approach',
    'avoid',
    'prepare',
    'build',
    'achieve',
    'believe',
    'receive',
    'seem',
    'discuss',
    'realize',
    'contain',
    'follow',
    'refer',
    'solve',
    'describe',
    'prefer',
    'prevent',
    'discover',
    'ensure',
    'expect',
    'invest',
    'reduce',
    'speak',
    'appear',
    'explain',
    'explore',
    'involve',
    'lose',

    # Adjectives
    'different',
    'used',
    'important',
    'every',
    'large',
    'available',
    'popular',
    'able',
    'basic',
    'known',
    'various',
    'difficult',
    'several',
    'united',
    'historical',
    'hot',
    'useful',
    'mental',
    'scared',
    'additional',
    'emotional',
    'old',
    'political',
    'similar',
    'healthy',
    'financial',
    'medical',
    'traditional',
    'federal',
    'entire',
    'strong',
    'actual',
    'significant',
    'successful',
    'electrical',
    'expensive',
    'pregnant',
    'intelligent',
    'interesting',
    'poor',
    'happy',
    'responsible',
    'cute',
    'helpful',
    'recent',
    'willing',
    'nice',
    'wonderful',
    'impossible',
    'serious',
    'huge',
    'rare',
    'technical',
    'typical',
]


def calculate_similarities(word, nlp):
    doc = nlp(word)
    all_similarities = []
    for i in other_words:
        i_doc = nlp(i)
        i_similarity = doc.similarity(i_doc)
        all_similarities.append(i_similarity)

    target_similarities = []
    for i in target_words:
        i_doc = nlp(i)
        i_similarity = doc.similarity(i_doc)
        target_similarities.append(i_similarity)

    return all_similarities, target_similarities

def generate_histogram(word, all_similarities):
    plt.gcf().clear()
    histogram_values = np.array(all_similarities)
    plt.hist(histogram_values, bins=[0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
    plt.title("".format(
                word))
    plt.savefig('similarities_to_{}.pdf'.format(word),
                format='pdf')

def generate_statistics(nlp):
    target_sim_all = []
    for idx, i in enumerate(target_words):
        all_sim, targ_sim = calculate_similarities(i, nlp)
        generate_histogram(i, all_sim)
        target_sim_all.append(targ_sim)

    #print(np.array(target_sim_all))
    df = pd.DataFrame(np.array(target_sim_all),
                        index=target_words,
                        columns=target_words)
    print(df)
    df.to_csv('sentiment_target_words.csv')

#def parse_args():
#    args = []
#    return args

#def main(args):
def main():
    nlp = spacy.load('en')
    generate_statistics(nlp)
    

if __name__ == '__main__':
    #args = parse_args()
    #main(args)
    main()
