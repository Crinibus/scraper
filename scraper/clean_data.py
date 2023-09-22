import logging
from sqlmodel import Session, select, col
from scraper.database import engine, Product, DataPoint


def clean_datapoints() -> None:
    print("Cleaning data...")
    logging.getLogger(__name__).info("Cleaning database datapoints")

    with Session(engine) as session:
        all_products = session.exec(select(Product)).all()

        for product in all_products:
            datapoints = session.exec(
                select(DataPoint).where(DataPoint.productId == product.productId).order_by(col(DataPoint.date).asc())
            ).all()

            for index, datapoint in enumerate(datapoints):
                if index in (0, len(datapoints) - 1):
                    continue

                previous_datapoint = datapoints[index - 1]
                next_datapoint = datapoints[index + 1]

                if datapoint.price == previous_datapoint.price and datapoint.price == next_datapoint.price:
                    session.delete(datapoint)
        session.commit()

    print("Done cleaning data")
