import plotly.graph_objects as go
from test_data.mock_data import get_users_mock_data, get_messages_mock_data
from core.utils import convert_user_stats_to_records, convert_messages_to_records


def demo_user_plot():
    mock = get_users_mock_data(bot_id=200, user_type="all", interval="day", mirror=False)
    records = convert_user_stats_to_records(mock)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=[r.time for r in records], y=[r.active for r in records], name="Active"))
    fig.add_trace(go.Scatter(x=[r.time for r in records], y=[r.inactive for r in records], name="Inactive"))
    fig.update_layout(title="User Stats Demo (bot=200, interval=day)")
    fig.write_html("test_users_plot.html", auto_open=True)


def demo_message_plot():
    mock = get_messages_mock_data(bot_id=200, msg_type="all", interval="week")
    records = convert_messages_to_records(mock)
    fig = go.Figure()
    fig.add_trace(go.Bar(x=[r.time for r in records], y=[r.total for r in records], name="Total Messages"))
    fig.update_layout(title="Message Stats Demo (bot=200, interval=week)")
    fig.write_html("test_messages_plot.html", auto_open=True)


if __name__ == "__main__":
    demo_user_plot()
    demo_message_plot()
