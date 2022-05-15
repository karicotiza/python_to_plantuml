import recognizer
import model_injector
import listener

if __name__ == '__main__':
    model_injector = model_injector.ModelInjector("model")
    recognizer = recognizer.Recognizer(model_injector.get_models())
    listener = listener.Listener(recognizer)

    # for _ in range(10):
    # output = listener.listen_file("audio/ru_3.opus")
    # print(output)

    for _ in range(3):
        output = listener.listen_microphone()
        print(output)
