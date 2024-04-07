import sys
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import clean_helper as c

# function for data preparation
def data_preparation():
    df = pd.read_csv('data/data.csv', encoding='latin-1')
    kamus_alay = c.kamus_alay()
    kamus_abusive = c.kamus_abusive()

    df['Tweet'] = df['Tweet'].apply(c.clean)
    df['Tweet'] = df['Tweet'].apply(lambda tweet: c.word_substitute(tweet, kamus_alay))
    df['total_abusive_word'] = df['Tweet'].apply(lambda tweet: c.total_abusive(tweet, kamus_abusive))
    df['text_abusive_word'] = df['Tweet'].apply(lambda tweet: c.text_abusive_word(tweet, kamus_abusive))

    df_clean = pd.DataFrame(df)

    df_clean.to_csv('output/data_preparation.csv', index=False)

# function for statistic and visualization
def report():
    # create csv for statistic report
    df = pd.read_csv('output/data_preparation.csv', encoding='latin-1')
    abusive_df = df.loc[df['total_abusive_word'] > 1, 'total_abusive_word']
    abusive_total = abusive_df.count()
    abusive_max = abusive_df.max()
    abusive_min = abusive_df.min()
    abusive_mean = abusive_df.mean()
    abusive_mode = abusive_df.mode().to_string(index=False)
    abusive_median = abusive_df.median()
    abusive_range = abusive_max - abusive_min
    abusive_min_outlier = c.check_min_outliers(abusive_df)
    abusive_max_outlier = c.check_max_outliers(abusive_df)
    abusive_variance = abusive_df.var()
    abusive_std = abusive_df.std()
    abusive_skew = abusive_df.skew()
    abusive_kurtosis = abusive_df.kurtosis()
    data = {
        "Stats" : ["Total Tweet Abusive", "Max","Min","Mean","Mode","Median","Range","Min Outlier","Max Outlier","Variance","Standard Deviation","Skewnes","Kurtosis"],
        "Value" : [abusive_total, abusive_max, abusive_min, abusive_mean, abusive_mode, abusive_median, abusive_range, abusive_min_outlier, abusive_max_outlier, abusive_variance, abusive_std, abusive_skew, abusive_kurtosis]
    }
    df_report = pd.DataFrame(data)
    df_report.to_csv('output/report_statistic.csv', index=False)

    # get only tweet that has abusive word to show
    df_data = df.loc[df['total_abusive_word'] > 1, ['total_abusive_word', 'HS_Weak', 'HS_Moderate', 'HS_Strong', 'HS', 'HS_Individual','HS_Group','HS_Religion','HS_Race','HS_Physical','HS_Gender','HS_Other','text_abusive_word']]
    
    # Pie report, percentase total kata abusive yang muncul dengan level hate speach
    labels = 'No HS', 'HS Weak', 'HS Moderate', 'HS Strong'
    sizes = [
        df_data.loc[df['HS'] == 0, 'total_abusive_word'].sum(), 
        df_data.loc[df['HS_Weak'] == 1, 'total_abusive_word'].sum(),  
        df_data.loc[df['HS_Moderate'] == 1, 'total_abusive_word'].sum(),  
        df_data.loc[df['HS_Strong'] == 1, 'total_abusive_word'].sum(), 
    ]
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%')
    plt.savefig('output/pie-total-abusive-word-per-hs-level.png')

    # create bar plot for Total Abusive Word by Hate Speech Level
    fig, ax = plt.subplots()
    ax.bar(labels, sizes, width=0.5)
    ax.set_ylabel('Total Word')
    ax.set_title('Total Abusive Word by Hate Speech Level')
    plt.savefig('output/bar-total-abusive-word-per-hs-level.png')


    # create bar plot for Total Abusive Word by Hate Speech Category
    fig, ax = plt.subplots(figsize=(9, 3))
    hs = ['HS_Individual','HS_Group','HS_Religion','HS_Race','HS_Physical','HS_Gender','HS_Other']
    counts = [
        df_data.loc[df['HS_Individual'] == 1, 'total_abusive_word'].sum(), 
        df_data.loc[df['HS_Group'] == 1, 'total_abusive_word'].sum(),  
        df_data.loc[df['HS_Religion'] == 1, 'total_abusive_word'].sum(),  
        df_data.loc[df['HS_Race'] == 1, 'total_abusive_word'].sum(), 
        df_data.loc[df['HS_Physical'] == 1, 'total_abusive_word'].sum(),  
        df_data.loc[df['HS_Gender'] == 1, 'total_abusive_word'].sum(),  
        df_data.loc[df['HS_Other'] == 1, 'total_abusive_word'].sum(), 
    ]

    ax.bar(hs, counts, width=0.5)
    ax.set_ylabel('Total Word')
    ax.set_title('Total Abusive Word by Hate Speech Category')
    plt.savefig('output/bar-chart-total-abusive-word-per-hs-category.png')


    # create bar plot for Total Tweet by Total Abusive Word
    total_tweet = df_data.groupby('total_abusive_word').size()
    fig, ax = plt.subplots()
    labels = []
    sizes = []
    for i, t in total_tweet.items():
        labels.append(i)
        sizes.append(t)
    # Create bar plot using Seaborn
    sns.barplot(x='Total Abusive Word', y='Total Tweet', data=pd.DataFrame({
        'Total Abusive Word': labels,
        'Total Tweet': sizes 
    }))
    ax.set_title('Total Tweet by Total Abusive Word')
    plt.savefig('output/bar-total-tweet-per-total-abusive-word.png')

    # create wordcloud for Most Abusive Word
    fig, ax = plt.subplots()
    text = ' '.join(df_data['text_abusive_word'])
    wordcloud = WordCloud().generate(text)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.savefig('output/wordcloud-most-abusive-word.png')
    
    return


if __name__ == "__main__":
    function_name = sys.argv[1]

    if function_name == "data_preparation":
        data_preparation()
    elif function_name == "report":
        report()
    else:
        print("Function not found")
