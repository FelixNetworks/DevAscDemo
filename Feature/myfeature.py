from dataclasses import dataclass, field
import argparse
import logging
from typing import Dict

"""
myfeature.py

A minimal, self-contained "feature" module.

Provides:
- Feature: a small configurable feature class with enable/disable and a simple `process` method.
- CLI entrypoint to run the feature against an input string.

Usage:
    python myfeature.py --mode uppercase "hello"
    python myfeature.py --mode reverse --disable "Hello World"
"""


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class Feature:
    name: str = "myfeature"
    enabled: bool = True
    config: Dict[str, str] = field(default_factory=lambda: {"mode": "uppercase"})

    def enable(self) -> None:
        self.enabled = True
        logger.debug("Feature enabled")

    def disable(self) -> None:
        self.enabled = False
        logger.debug("Feature disabled")

    def update_config(self, **kwargs) -> None:
        self.config.update(kwargs)
        logger.debug("Config updated: %s", self.config)

    def process(self, text: str) -> str:
        """
        Process the input text based on the configured mode.
        Supported modes: 'uppercase', 'lowercase', 'reverse', 'title'
        """
        logger.debug("Processing text: %r with config: %s", text, self.config)
        if not self.enabled:
            logger.info("Feature is disabled; returning original text")
            return text

        mode = self.config.get("mode", "uppercase").lower()
        if mode == "uppercase":
            return text.upper()
        if mode == "lowercase":
            return text.lower()
        if mode == "reverse":
            return text[::-1]
        if mode == "title":
            return text.title()

        logger.warning("Unknown mode %r; returning original text", mode)
        return text


def main() -> None:
    parser = argparse.ArgumentParser(description="Run myfeature on a string.")
    parser.add_argument("input", help="Input string to process")
    parser.add_argument("--mode", choices=["uppercase", "lowercase", "reverse", "title"],
                        default="uppercase", help="Processing mode")
    parser.add_argument("--disable", action="store_true", help="Start with the feature disabled")
    parser.add_argument("--name", default="myfeature", help="Feature instance name")
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable debug logging")
    args = parser.parse_args()

    if args.verbose:
        logger.setLevel(logging.DEBUG)

    feat = Feature(name=args.name, enabled=not args.disable, config={"mode": args.mode})
    result = feat.process(args.input)
    print(result)


if __name__ == "__main__":
    main()