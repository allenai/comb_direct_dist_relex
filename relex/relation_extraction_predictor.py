from typing import Tuple

import logging
from overrides import overrides
from allennlp.common.util import JsonDict
from allennlp.data import Instance
from allennlp.predictors.predictor import Predictor

log = logging.getLogger(__name__)  # pylint: disable=invalid-name

@Predictor.register('relex')
class RelationExtractionPredictor(Predictor):
    """"Predictor wrapper for the RelationExtractionPredictor"""
    @overrides
    def _json_to_instance(self, json_dict: JsonDict) -> Tuple[Instance, JsonDict]:
        e1 = json_dict['e1']
        e2 = json_dict['e2']
        mentions = json_dict['mentions']

        instance = self._dataset_reader.text_to_instance(
                e1=e1, e2=e2, rels=[], mentions=mentions, is_predict=True, is_supervised_bag=False)
        # label_dict will be like {0: "ACL", 1: "AI", ...}
        # label_dict = self._model.vocab.get_index_to_token_vocabulary('labels')
        # Convert it to list ["ACL", "AI", ...]
        # all_labels = [label_dict[i] for i in range(len(label_dict))]
        if not instance:
            log.error('parsing instance failed: %s', mentions)
            instance = self._dataset_reader.text_to_instance(
                    e1="e1", e2="e2", rels=[],
                    mentions=["Some relation between <e1>entity 1</e1> and <e2>entity 2</e2>"],
                    is_predict=True, is_supervised_bag=False)
        return instance, {}# {"all_labels": all_labels}
