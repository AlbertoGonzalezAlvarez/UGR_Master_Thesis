import locale
import string

import pandas as pd
import numpy as np

import config

locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

analyzed_interventions = pd.read_json('./assets/reduced_df.gzip',
                                      compression='gzip', convert_dates=['fecha'])


def get_intervention_count():
    return analyzed_interventions['organizacion'].value_counts()


def get_woman_interventions():
    woman_interventions_per_party = analyzed_interventions['organizacion'].loc[analyzed_interventions['sexo'] == 'M'] \
        .value_counts()
    return woman_interventions_per_party.divide(get_intervention_count(), fill_value=0.0) * 100


def get_n_deputies():
    return analyzed_interventions[['organizacion', 'diputado']].drop_duplicates(subset=['diputado'])['organizacion'] \
        .value_counts()


def get_n_woman_deputies():
    return analyzed_interventions[['organizacion', 'diputado']].loc[analyzed_interventions['sexo'] == 'M'] \
               .drop_duplicates(subset=['diputado'])['organizacion'].value_counts() \
               .divide(get_n_deputies(), fill_value=0.0) * 100


def get_topic_distribution_per_party():
    org_topic_distribution = analyzed_interventions[[*config.TOPIC_NAMES, 'organizacion']] \
        .groupby('organizacion', as_index=False).mean()

    party_topic_distribution = org_topic_distribution[org_topic_distribution['organizacion'].isin(config.PARTY_ABBREVS)]
    unpivoted_topic_distribution = pd.melt(party_topic_distribution, id_vars=['organizacion'], var_name='topic',
                                           value_name='score')

    return unpivoted_topic_distribution


def get_topic_distribution_per_sex():
    distribution_per_sex = analyzed_interventions[[*config.TOPIC_NAMES, 'sexo']].groupby('sexo', as_index=False).mean()
    return pd.melt(distribution_per_sex, id_vars=['sexo'], var_name='topic', value_name='score')


def get_max_time_per_topic():
    selected_cols = ['predominant_topic', 'organizacion', 'diputado', 'fecha', *config.TOPIC_TIMES]
    longest_intervention_time_idx_topic = analyzed_interventions[config.TOPIC_TIMES].idxmax()
    max_time_per_topic_df = analyzed_interventions[selected_cols].iloc[longest_intervention_time_idx_topic]
    max_time_per_topic_df['score'] = np.diag(max_time_per_topic_df[config.TOPIC_TIMES])

    return max_time_per_topic_df


def get_monthly_evolution_topics():
    formatted_dates = analyzed_interventions.fecha.dt.strftime("%B-%Y").transform(string.capwords)

    monthly_topic_scores = analyzed_interventions.groupby([formatted_dates, 'organizacion'], sort=False)[config.TOPIC_NAMES]
    monthly_topic_scores_mean = monthly_topic_scores.apply(pd.DataFrame.mean).reset_index()

    return monthly_topic_scores_mean
