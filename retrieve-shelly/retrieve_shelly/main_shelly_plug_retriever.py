import logging
from retrieve_shelly.core.logging_config import configure_logging
from retrieve_shelly.core.shelly_plug_retriever import POLL_INTERVAL_SECONDS, ShellyPlugRetriever

configure_logging()
logger = logging.getLogger(__name__)

logger.info(f"Starting Shelly Plug S retrieval with POLL_INTERVAL_SECONDS={POLL_INTERVAL_SECONDS}")

plug_retriever = ShellyPlugRetriever()
plug_retriever.start_retrieval()
