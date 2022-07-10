import editdistance


class Evaluator:
    def __init__(self, case_sensitive=False):

        self.case_sensitive = case_sensitive
        self.get_edit_distance = editdistance.eval
        self.anls_threshold = 0.5

        self.total_accuracies = []
        self.total_anls = []

        self.best_accuracy = 0
        # self.best_anls = 0
        self.best_epoch = 0

    def get_metrics(self, gt_answers, preds, update_global_metrics=True):
        batch_accuracy = []
        batch_anls = []
        for batch_idx in range(len(preds)):
            gt = [self._preprocess_str(gt_elm) for gt_elm in gt_answers[batch_idx]]
            pred = self._preprocess_str(preds[batch_idx])

            batch_accuracy.append(self._calculate_accuracy(gt, pred))
            batch_anls.append(self._calculate_anls(gt, pred))

        # if accumulate_metrics:
        #     self.total_accuracies.extend(batch_accuracy)
        #     self.total_anls.extend(batch_anls)

        return {'accuracy': batch_accuracy, 'anls': batch_anls}

    def get_retrieval_metric(self, gt_answer_page, pred_answer_page):

        if pred_answer_page is None:
            retrieval_precision = [0 for gt in gt_answer_page]

        else:
            retrieval_precision = [1 if gt == pred else 0 for gt, pred in zip(gt_answer_page, pred_answer_page)]

        return retrieval_precision


    def update_global_metrics(self, accuracy, anls, current_epoch):
        if accuracy > self.best_accuracy:
            self.best_accuracy = accuracy
            self.best_epoch = current_epoch
            return True

        else:
            return False

    def _preprocess_str(self, string):
        if not self.case_sensitive:
            string = string.lower()

        return string.strip()

    def _calculate_accuracy(self, gt, pred):
        for gt_elm in gt:
            if gt_elm == pred:
                return 1

        return 0

    def _calculate_anls(self, gt, pred):
        if len(pred) == 0:
            return 0

        answers_similarity = [1 - self.get_edit_distance(gt_elm, pred) / max(len(gt_elm), len(pred)) for gt_elm in gt]

        try:
            max_similarity = max(answers_similarity)
        except ValueError:
            a = 0

        anls = max_similarity if max_similarity >= self.anls_threshold else 0
        return anls


if __name__ == '__main__':

    m = Evaluator()
    m.get_metrics(['aa', 'ab'], 'bb')


