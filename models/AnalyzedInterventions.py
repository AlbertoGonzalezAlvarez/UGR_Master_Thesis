import locale
import string

import pandas as pd

import config

locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

analyzed_interventions = pd.read_json('./assets/analyzed_interventions_separated_cols_w_topic_times.gzip',
                                      compression='gzip', convert_dates=['fecha'])


def get_intervention_count():
	return analyzed_interventions['organizacion'].value_counts()


def get_woman_interventions():
	woman_interventions_per_party = analyzed_interventions['organizacion'].loc[analyzed_interventions['sexo'] == 'M']\
		       .value_counts()
	return woman_interventions_per_party.divide(get_intervention_count(), fill_value=0.0) * 100


def get_n_deputies():
	return analyzed_interventions[['organizacion', 'diputado']].drop_duplicates(subset=['diputado'])['organizacion']\
		.value_counts()


def get_n_woman_deputies():
	return analyzed_interventions[['organizacion', 'diputado']].loc[analyzed_interventions['sexo'] == 'M']\
		       .drop_duplicates(subset=['diputado'])['organizacion'].value_counts()\
		       .divide(get_n_deputies(), fill_value=0.0) * 100


def topic_distribution_per_party():
	org_topic_distribution = analyzed_interventions[[*config.TOPIC_NAMES, 'organizacion']] \
		.groupby('organizacion', as_index=False).mean()

	party_topic_distribution = org_topic_distribution[org_topic_distribution['organizacion'].isin(config.PARTY_ABBREVS)]
	unpivoted_topic_distribution = pd.melt(party_topic_distribution, id_vars=['organizacion'], var_name='topic',
	                                       value_name='score')

	# fig = px.bar(unpivoted_topic_distribution, x="topic", y="score", color="organizacion", color_discrete_sequence=PARTY_COLORS, barmode='group', template='lux',
	#              category_orders={'organizacion': list(PARTY_CONFIG.keys())})
	# fig.show()

	return unpivoted_topic_distribution


def topic_distribution_per_sex():
	distribution_per_sex = analyzed_interventions[[*config.TOPIC_NAMES, 'sexo']].groupby('sexo', as_index=False).mean()
	return pd.melt(distribution_per_sex, id_vars=['sexo'], var_name='topic', value_name='score')


def max_time_per_topic():
	selected_cols = ['predominant_topic', 'organizacion', 'intervention_time', 'diputado', 'fecha'] + config.TOPIC_NAMES
	longest_intervention_time_idx_topic = analyzed_interventions[config.TOPIC_NAMES].idxmax()
	return analyzed_interventions[selected_cols].iloc[longest_intervention_time_idx_topic]


# def monthly_topics():
# 	date_range = analyzed_interventions.fecha.dt.strftime("%B-%Y").transform(string.capwords).unique()
# 	formatted_dates = analyzed_interventions.fecha.dt.strftime("%B-%Y").transform(string.capwords)
#
# 	monthly_topics_scores = analyzed_interventions.groupby([formatted_dates, 'organizacion'], sort=False)[config.TOPIC_NAMES]\
# 		.apply(pd.DataFrame.mean).reset_index()
#
# 	party_monthly_topic_scores = monthly_topics_scores.groupby('organizacion', sort=False)
# 	party_monthly_data = {}
#
# 	for party_id, party_df in party_monthly_topic_scores:
# 		initialized_df = pd.DataFrame(config.TOPIC_NAMES, index=date_range)
# 		initialized_df.update(party_df.set_index('fecha'))
# 		party_monthly_data[party_id] = initialized_df
#
# 	return party_monthly_data
