import os


class ModelInjector:
    def __init__(self, path_to_directory_with_models: str):
        self.models = os.listdir(path_to_directory_with_models)
        for index in range(len(self.models)):
            self.models[index] = os.path.join(path_to_directory_with_models, self.models[index])

    def get_models(self):
        return self.models
