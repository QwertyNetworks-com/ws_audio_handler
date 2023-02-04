class ParsePath:
    def __init__(self, path: str):
        speaker = path.rsplit("speaker/", 1)[1]
        if "viewer" in path:
            status = "viewer"
            username = path.split("viewer/", 1)[1].rsplit("/speaker", 1)[0]
        else:
            status = "speaker"
            username = path.rsplit("/", 1)[1]

        self.username = username
        self.user_status = status
        self.speaker = speaker
