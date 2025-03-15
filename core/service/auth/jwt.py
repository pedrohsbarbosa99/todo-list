import base64
import hashlib
import hmac
import json
from datetime import datetime, timedelta

from core import config


class JWT:
    def __sanitize(self, token):
        return token.split(" ")[1]

    def is_valid(self, token):
        if "." not in token or len(token.split(".")) != 3 or len(token.split(" ")) != 2:
            return False

        jwt_token = token.split(" ")[1]

        header_b64, payload_b64, signature_b64 = jwt_token.split(".")

        signature = base64.urlsafe_b64decode(signature_b64 + "==")

        header_payload = header_b64 + "." + payload_b64

        recalculated_signature = hmac.new(
            config.SECRET_KEY.encode(),
            header_payload.encode(),
            hashlib.sha256,
        ).digest()

        return hmac.compare_digest(recalculated_signature, signature)

    def encode(self, payload):
        payload["exp"] = int((datetime.now() + timedelta(days=1)).timestamp())
        payload["iat"] = int(datetime.now().timestamp())
        jwt_header = {"alg": "HS256", "typ": "JWT"}

        jwt_values = {
            "header": jwt_header,
            "payload": payload,
        }

        jwt_values_cleaned = {
            key: json.dumps(
                value,
                separators=(",", ":"),
            )
            for key, value in jwt_values.items()
        }

        jwt_values_enc = {
            key: base64.urlsafe_b64encode(value.encode()).decode().rstrip("=")
            for key, value in jwt_values_cleaned.items()
        }

        sig_payload = "{header}.{payload}".format(
            header=jwt_values_enc["header"],
            payload=jwt_values_enc["payload"],
        )

        sig = hmac.new(
            bytes(config.SECRET_KEY, "utf-8"),
            msg=sig_payload.encode(),
            digestmod=hashlib.sha256,
        ).digest()

        ecoded_sig = base64.urlsafe_b64encode(sig).decode().rstrip("=")

        token = "{sig_payload}.{sig}".format(
            sig_payload=sig_payload,
            sig=ecoded_sig,
        )

        return token

    def decode(self, token):
        if not self.is_valid(token):
            raise Exception("Invalid token")

        token = self.__sanitize(token)

        header_b64, payload_b64, _ = token.split(".")

        header_json = base64.urlsafe_b64decode(header_b64 + "==").decode("utf-8")
        header = json.loads(header_json)

        payload_json = base64.urlsafe_b64decode(payload_b64 + "==").decode("utf-8")
        payload = json.loads(payload_json)

        return header, payload
