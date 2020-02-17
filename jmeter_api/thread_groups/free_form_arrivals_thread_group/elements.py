from xml.etree.ElementTree import Element
from typing import List

from jmeter_api.basics.thread_group.bzm_elements import BasicBzmThreadGroup, ThreadGroupAction, Unit
from jmeter_api.basics.utils import Renderable, IncludesElements, tree_to_str


class FreeFormArrivalsThreadGroup(BasicBzmThreadGroup, Renderable):

    root_element_name = 'com.blazemeter.jmeter.threads.arrivals.FreeFormArrivalsThreadGroup'

    def __init__(self, *,
                 schedule: List[str],
                 iterations: int = None,
                 concurrency_limit: int = None,
                 log_filename: str = None,
                 unit:  Unit = Unit.MINUTE,
                 on_sample_error: ThreadGroupAction = ThreadGroupAction.CONTINUE,
                 name: str = 'bzm - Free-Form Arrivals Thread Group',
                 comments: str = '',
                 is_enabled: bool = True):
        self.schedule = schedule
        self.iterations = iterations
        self.concurrency_limit = concurrency_limit
        BasicBzmThreadGroup.__init__(self,
                                     log_filename=log_filename,
                                     unit=unit,
                                     on_sample_error=on_sample_error,
                                     name=name,
                                     comments=comments,
                                     is_enabled=is_enabled)

    @property
    def schedule(self):
        return self._schedule

    @schedule.setter
    def schedule(self, value: int):
        if not isinstance(value, List):
            raise TypeError(
                f'schedule must be positive int. continue_forever {type(value)} = {value}')
        else:
            self._schedule = value

    @property
    def iterations(self) -> str:
        return self._iterations

    @iterations.setter
    def iterations(self, value: int):
        if value is None:
            self._iterations = ""
        elif not isinstance(value, int) or value < 0:
            raise TypeError(
                f'iterations must be positive int. continue_forever {type(value)} = {value}')
        else:
            self._iterations = str(value)

    @property
    def concurrency_limit(self) -> str:
        return self._concurrency_limit

    @concurrency_limit.setter
    def concurrency_limit(self, value: int):
        if value is None:
            self._concurrency_limit = ""
        elif not isinstance(value, int) or value < 0:
            raise TypeError(
                f'concurrency_limit must be positive int. continue_forever {type(value)} = {value}')
        else:
            self._concurrency_limit = str(value)
            
    def to_xml(self) -> str:
        element_root, xml_tree = super()._add_basics()

        for element in list(element_root):
            try:
                if element.attrib['name'] == 'ThreadGroup.on_sample_error':
                    element.text = self.on_sample_error.value
                elif element.attrib['name'] == 'Schedule':
                    #element.text = self.target_rate
                elif element.attrib['name'] == 'LogFilename':
                    element.text = self.log_filename
                elif element.attrib['name'] == 'Unit':
                    element.text = self.unit.value
                elif element.attrib['name'] == 'Iterations':
                    element.text = self.iterations
                elif element.attrib['name'] == 'ConcurrencyLimit':
                    element.text = self.concurrency_limit
            except KeyError:
                continue
        content_root = xml_tree.find('hashTree')
        content_root.text = self._render_inner_elements()
        return tree_to_str(xml_tree)
