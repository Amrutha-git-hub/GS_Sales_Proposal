import os 


def load_env_variables():
    os.environ['GOOGLE_API_KEY'] = 'AIzaSyDTYADVQVxJ5-UKQYZ8-tNFDlo-SKhwzEU'
    # SERP_API_KEY = 0900f7a2f830083d80385bc46c1ff1f1e6626da3f568de640fe13759e9655450
    os.environ['FILE_SAVE_PATH'] = "SalesProposalsDocs/Files"
    os.environ['HROMA_PATH'] = "SalesPropsalsDocs/chroma"
    os.environ['OUTPUT_PATH'] = "SalesProposalsGenerated"

                    