from datetime import date
from repositories.transaction_repository import TransactionRepository
from services.transaction_service import TransactionService
from sqladmin import BaseView, expose
import matplotlib.pyplot as plt
import base64
import pandas as pd
import io
import matplotlib.dates as mdates


class StatisticView(BaseView):
    name = "Statistic Page"
    icon = "fa-solid fa-chart-line"

    @expose("/statistic", methods=["GET"])
    async def report_page(
        self,
        request,
    ):
        service = TransactionService(TransactionRepository())
        service.set_service_db_session(request.state.db_session)

        start_date = request.query_params.get("start_date", None)
        end_date = request.query_params.get("end_date", None)

        start_date_obj = date.fromisoformat(start_date) if start_date else None
        end_date_obj = date.fromisoformat(end_date) if end_date else None

        data = await service.get_transaction_sum(start_date_obj, end_date_obj)
        transactions = await service.get_transactions(start_date_obj, end_date_obj)
        if len(transactions) > 0:
            graph = await self.transaction_graph(transactions)
        else:
            graph = None
        return await self.templates.TemplateResponse(
            request,
            "statistic.html",
            context={
                "count": data["count"],
                "total_sum": data["total_sum"],
                "graph": graph,
                "start_date": start_date_obj,
                "end_date": end_date_obj,
            },
        )

    async def transaction_graph(self, transactions):
        df = pd.DataFrame(transactions)

        df["date"] = pd.to_datetime(df["date"]).dt.date

        grouped = df.groupby(["date", "transaction_type"]).sum().reset_index()

        fig, ax = plt.subplots(figsize=(12, 6))

        for transaction_type in grouped["transaction_type"].unique():
            subset = grouped[grouped["transaction_type"] == transaction_type]
            ax.plot(
                subset["date"],
                subset["total_amount"],
                label=transaction_type,
                marker="o",
                linestyle="-",
            )

        ax.set_xlabel("Date")
        ax.set_ylabel("Total Amount")
        ax.set_title("Total Transaction Amounts by Date and Type")

        ax.xaxis.set_major_locator(mdates.AutoDateLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
        fig.autofmt_xdate()

        ax.legend()

        buffer = io.BytesIO()
        plt.savefig(buffer, format="png", bbox_inches="tight")
        buffer.seek(0)
        img_base64 = base64.b64encode(buffer.read()).decode()
        plt.close(fig)

        return f"data:image/png;base64,{img_base64}"
