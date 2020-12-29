import locale
import string

import pandas as pd

from config.AppConfig import N_TOPICS

locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

topic_idx_names = [f'topic_{i}' for i in range(0, N_TOPICS)]
topic_time_names = [f'topic_{i}_time' for i in range(0, N_TOPICS)]

# Dataframe ordered by date
# TODO: map strings to numbers and create another df
analyzed_interventions = pd.read_json('./assets/analyzed_interventions.gzip', compression='gzip', convert_dates=['fecha'])
analyzed_interventions = analyzed_interventions.convert_dtypes()

float_downcast_columns = topic_idx_names + topic_time_names
analyzed_interventions[float_downcast_columns] = analyzed_interventions[float_downcast_columns].apply(
	pd.to_numeric, downcast='float')


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
	return analyzed_interventions[topic_idx_names + ['organizacion']].groupby(
		'organizacion').mean()


def topic_distribution_per_sex():
	return analyzed_interventions[topic_idx_names + ['sexo']].groupby('sexo').mean()


def max_time_per_topic():
	return analyzed_interventions[
		['predominant_topic', 'organizacion', 'intervention_time', 'diputado', 'fecha'] + topic_time_names]\
			.iloc[analyzed_interventions[topic_time_names].idxmax()]


def monthly_topics(computation_function):
	date_range = analyzed_interventions.fecha.dt.strftime("%B-%Y").transform(string.capwords).unique()
	data_columns = dict.fromkeys(topic_idx_names, 0)

	monthly_topics_scores = analyzed_interventions.groupby(
		[
			analyzed_interventions.fecha.dt.strftime("%B-%Y").transform(string.capwords),
			'organizacion'
		]
		, sort=False)[topic_idx_names].apply(computation_function).reset_index()

	party_topic_scores_per_month = monthly_topics_scores.groupby('organizacion', sort=False)
	party_monthly_data = {}

	for party_id, party_df in party_topic_scores_per_month:
		initialized_df = pd.DataFrame(data_columns, index=date_range)
		initialized_df.update(party_df.set_index('fecha'))
		party_monthly_data[party_id] = initialized_df

	return party_monthly_data