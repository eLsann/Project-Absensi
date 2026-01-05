# Package marker for external_model to ensure imports like
# `external_model.src.recognizer` work reliably inside Docker containers.
# Keeping this explicit __init__ avoids subtle namespace/package resolution issues.
