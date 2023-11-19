#%%
import yaml
#%%
def load_credentials(file_path='credentials.yaml'):
    with open(file_path, 'r') as file:
        credentials = yaml.safe_load(file)
    return credentials
#%%
credentials = pd.DataFrame(credentials)
# %%
