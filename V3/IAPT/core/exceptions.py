class IAPTError(Exception):
    def __init__(
        self,
        message,
        error=None,
        file_path=None,
        student_count=None,
        results_count=None,
        homework_count=None,
        student_ids=None,
        student_id=None,
    ):
        super().__init__(message)
        self.message = message
        self.details = error
        self.file_path = file_path
        self.student_count = student_count
        self.results_count = results_count
        self.homework_count = homework_count
        self.student_id = student_id
        self.student_ids = student_ids
