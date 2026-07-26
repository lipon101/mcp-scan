# A deliberately insecure, poorly-packaged server (mcp-grade's 'bad' fixture).
# DO NOT copy these patterns.
#
# NOTE: the value below is a FAKE placeholder used only to demonstrate secret
# detection. It is intentionally NOT shaped like a real provider key, so GitHub
# secret scanning will not raise a false positive on this example repo — but
# mcp-grade's generic "hardcoded secret" check still (correctly) flags it.

API_KEY = "FAKE_EXAMPLE_API_KEY_0000000000"  # hardcoded secret — bad! (fake value)


def handle(request):
    # eval on untrusted input — bad!
    return eval(request.get("expr", "0"))


if __name__ == "__main__":
    print(handle({"expr": "1+1"}))
