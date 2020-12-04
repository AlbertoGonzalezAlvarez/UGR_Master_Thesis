import locale
import string

import pandas as pd
from gensim.models import LdaModel

from config.AppConfig import N_TOPICS

locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
lda_model = LdaModel.load('./assets/model_t15_a051_b001/lda.model')

# Dataframe ordered by date
analyzed_interventions = pd.read_json('./assets/analyzed_interventions_separated_cols_w_topic_times.gzip',
                                      compression='gzip', convert_dates=['fecha'])


def get_parties_info():
	n_interventions = analyzed_interventions['organizacion'] \
		.value_counts()

	n_deputies = analyzed_interventions[['organizacion', 'diputado']] \
		.drop_duplicates(subset=['diputado'])['organizacion'] \
		.value_counts()

	return {
		'n_interventions': n_interventions,
		'n_women_interventions': analyzed_interventions['organizacion']
			                         .loc[analyzed_interventions['sexo'] == 'M']
			                         .value_counts()
			                         .divide(n_interventions, fill_value=0.0) * 100,
		'n_deputies': n_deputies,
		'n_women_deputies': analyzed_interventions[['organizacion', 'diputado']]
			                    .loc[analyzed_interventions['sexo'] == 'M']
			                    .drop_duplicates(subset=['diputado'])['organizacion']
			                    .value_counts()
			                    .divide(n_deputies, fill_value=0.0) * 100
	}


def topic_distribution_per_party():
	return analyzed_interventions[[f'topic_{i}' for i in range(0, N_TOPICS)] + ['organizacion']].groupby(
		'organizacion').mean()


def topic_distribution_per_sex():
	return analyzed_interventions[[f'topic_{i}' for i in range(0, N_TOPICS)] + ['sexo']].groupby('sexo').mean()


def max_time_per_topic():
	return analyzed_interventions[
		['predominant_topic', 'organizacion', 'intervention_time', 'diputado', 'fecha'] +
		[f'topic_{i}_time' for i in range(0, N_TOPICS)]
		].iloc[analyzed_interventions[[f'topic_{i}_time' for i in range(0, N_TOPICS)]].idxmax()]


def monthly_topics(computation_function):
	date_range = analyzed_interventions.fecha.dt.strftime("%B-%Y").transform(string.capwords).unique()
	data_columns = {
		'fecha': date_range,
		**{f'topic_{i}': 0 for i in range(0, N_TOPICS)}
	}

	monthly_topics_scores = analyzed_interventions.groupby(
		[
			analyzed_interventions.fecha.dt.strftime("%B-%Y").transform(string.capwords),
			'organizacion'
		]
		, sort=False)[[f'topic_{i}' for i in range(0, N_TOPICS)]].apply(computation_function).reset_index()

	party_topic_scores_per_month = monthly_topics_scores.groupby('organizacion', sort=False)
	party_monthly_data = {}
	initialized_df = pd.DataFrame(data_columns)

	for party_id in party_topic_scores_per_month.groups.keys():
		party_monthly_data[party_id] = party_topic_scores_per_month.get_group(party_id) \
			.combine_first(initialized_df).reindex(initialized_df.index)

	return party_monthly_data

monthly_topics(pd.DataFrame.mean)