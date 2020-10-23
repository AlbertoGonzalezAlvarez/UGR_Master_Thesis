import pandas as pd
from gensim.models import LdaModel


lda_model = LdaModel.load('./assets/model_t15_a051_b001/lda.model')
analyzed_interventions = pd.read_json('./assets/reduced_data_json.gzip', compression='gzip')
analyzed_interventions['fecha'] = pd.to_datetime(analyzed_interventions['fecha'])


def get_parties_info():
	n_interventions = analyzed_interventions['organizacion']\
		.value_counts()

	n_deputies = analyzed_interventions[['organizacion', 'diputado']]\
		.drop_duplicates(subset=['diputado'])['organizacion']\
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