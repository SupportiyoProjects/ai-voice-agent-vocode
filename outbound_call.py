import os
from dotenv import load_dotenv
import logging

load_dotenv()

from vocode.streaming.telephony.conversation.outbound_call import OutboundCall
from vocode.streaming.telephony.config_manager.redis_config_manager import RedisConfigManager
from vocode.streaming.models.agent import ChatGPTAgentConfig
from vocode.streaming.models.message import BaseMessage
from vocode.streaming.models.synthesizer import StreamElementsSynthesizerConfig

BASE_URL = os.environ["BASE_URL"]

# Set up logging
logging.basicConfig(level=logging.INFO)

def get_assistant_instructions():
    with open('instructions.txt', 'r') as file:
        return file.read()

async def main():
    config_manager = RedisConfigManager()

    # Use the same agent config as in main.py
    agent_config = ChatGPTAgentConfig(
        initial_message=BaseMessage(text="Hello, who am I talking to?"),
        prompt_preamble=get_assistant_instructions(),
        generate_responses=True,
    )

    # Add synthesizer config
    synthesizer_config = StreamElementsSynthesizerConfig.from_telephone_output_device()

    outbound_call = OutboundCall(
        base_url=BASE_URL,
        to_phone="+923318450446",
        from_phone="+16267092809",
        config_manager=config_manager,
        agent_config=agent_config,
        synthesizer_config=synthesizer_config
    )

    logging.info("Starting outbound call...")
    input("Press enter to start call...")
    await outbound_call.start()
    logging.info("Call ended.")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
