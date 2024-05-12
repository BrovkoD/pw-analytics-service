import flask
import torch
from neuralprophet import NeuralProphet

from dao import weather_factor_dao


def get_neural_net(data_freq, retrain, forecast_years):
    history_df = form_dataset(data_freq)
    m = prepare_neural_net(data_freq, retrain, history_df)

    # # # forecasting
    amount_to_forecast = int(get_periods(data_freq, forecast_years))
    future_df = m.make_future_dataframe(history_df,
                                        periods=amount_to_forecast,
                                        n_historic_predictions=len(history_df) - amount_to_forecast)
    forecast = m.predict(future_df)

    # return forecast.to_html()

    # plot = make_subplots(rows=2, cols=2)
    # plot.add_traces(m.plot(forecast).data, rows=1, cols=1)
    # plot.add_traces(m.plot_components(forecast).data, rows=2, cols=1)
    # plot.add_traces(m.plot_parameters().data, rows=2, cols=2)  # show params of the neural net
    # return plot.to_json(pretty=True)

    m.plot(forecast).show()
    m.plot_components(forecast).show()
    m.plot_parameters().show()
    return "Success"

    # plot = m.plot(forecast)
    # m.plot_components(forecast).show()
    # m.plot_parameters().show()
    # return plot.to_json(pretty=True)


def form_dataset(data_freq):
    if data_freq == "month":
        return weather_factor_dao.get_month_avg()

    elif data_freq == "day":
        return weather_factor_dao.get_day_avg()

    elif data_freq == "3h":
        return weather_factor_dao.get_3h()

    else:
        raise Exception("No data_freq = '%s' found for the data fetch" % data_freq)


def get_model_location(data_freq):
    return "resources/trained_models/" + data_freq + "_model.pt"


def prepare_neural_net(data_freq, retrain, history_df):
    if not retrain:
        try:
            m = torch.load(get_model_location(data_freq))
            m.restore_trainer()
            return m
        except FileNotFoundError:
            pass

    if data_freq == "month":
        m = NeuralProphet(yearly_seasonality=True)

    elif data_freq == "day":
        m = NeuralProphet(weekly_seasonality=True, yearly_seasonality=True)

    elif data_freq == "3h":
        m = NeuralProphet(seasonality_mode="multiplicative", daily_seasonality=True, weekly_seasonality=True,
                          yearly_seasonality=True)
    else:
        raise Exception("No data_freq = '%s' found for the neural network" % data_freq)

    # # # make results the same every time
    # set_random_seed(0)

    # # # train and save the neural network
    m.fit(history_df)
    torch.save(m, get_model_location(data_freq))

    return m


def get_periods(data_freq, years):
    if data_freq == "month":
        return 12 * years

    elif data_freq == "day":
        return 365 * years

    elif data_freq == "3h":
        return ((24 / 3) * 365) * years

    else:
        raise Exception("No data_freq = '%s' found for the periods" % data_freq)
