from mysite.data_visualization import Visualize, Utilities


def casing_the_characters(input_text):
    return_text = []
    for text in input_text:
        try:
            if text.isnumeric():
                return_text.append(Utilities().convert_int_to_text(text))
            else:
                return_text.append(text)
        except Exception as e:
            pass
    return return_text


columns_to_take = ["review"]


def csv_wrapper(func):
    def csv_inner_function(*args, **kwargs):
        # Reading from file
        input_data = args[0]

        index_to_capture = next(
            iter([list_index for list_index, value in enumerate(input_data[0]) if value in columns_to_take]), None)
        input_data = [rows[index_to_capture] for rows in input_data]
        kwargs["input_data"] = input_data[1:]

        inner_result, positive, negative = func(*args, **kwargs)
        return {"positive": positive, "negative": negative, "result": inner_result}

    return csv_inner_function


@csv_wrapper
def normalization(*args, **kwargs):
    input_data = kwargs["input_data"]
    outer_result = []
    positive, negative = (0, 0)
    for line in input_data:
        visualize_obj = Visualize(line)
        response = visualize_obj.process()
        text_assertion = response["assertion"]
        if text_assertion == "positive":
            positive = positive + 1
        else:
            negative = negative + 1

        outer_result.append([line, text_assertion])
    return outer_result, positive, negative


if __name__ == '__main__':
    result = normalization()
    print(result)
