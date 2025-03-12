# Crawler

The Crawler component is responsible for discovering data sources within a given scope. Subclasses of the crawler implement the logic required to traverse a defined starting point and identify valid data sources that can be used for import. This makes crawlers particularly useful when dealing with datasets that are distributed across multiple locations or systems.

While a crawler is a powerful tool for automating data source discovery, it is not strictly required for every import process. In cases where data sources are explicitly known and provided, a crawler may be unnecessary. However, when working with large-scale or distributed datasets, a crawler can significantly simplify and streamline the import process by reducing the need for manual source identification.