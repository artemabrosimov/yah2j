from jmeter_api.basics.pre_processor.elements import BasicPreProcessor
from jmeter_api.basics.utils import Renderable, tree_to_str

from xml.etree.ElementTree import tostring, SubElement
from xml.sax.saxutils import unescape
from typing import Union, List
import logging
from enum import Enum
import os


class ScriptLanguage(Enum):
    GROOVY = 'groovy'
    BEANSHELL = 'beanshell'
    BSH = 'bsh'
    ECMASCRIPT = 'ecmasript'
    JAVA = 'java'
    JS = 'javascript'
    JEXL = 'jexl'
    JEXL2 = 'jexl2'

class JSR223PreProcessor(BasicPreProcessor, Renderable):

    root_element_name = 'JSR223PreProcessor'

    def __init__(self, *,
                 cacheKey: bool = True,
                 filename: str = '',
                 parameters: str = '',
                 script: str = '',
                 scriptLanguage: ScriptLanguage = ScriptLanguage.GROOVY,
                 name: str = 'JSR223 PreProcessor',
                 comments: str = '',
                 is_enabled: bool = True
                 ):
        """

        :type source_type: object
        """
        self.cacheKey = cacheKey
        self.filename = filename
        self.parameters = parameters
        self.script = script
        self.scriptLanguage = scriptLanguage
        BasicPreProcessor.__init__(
            self, name=name, comments=comments, is_enabled=is_enabled)

    @property
    def filename(self):
        return self._filename

    @filename.setter
    def filename(self, value):
        if not isinstance(value, str):
            raise TypeError(
                f'arg: filename should be str. {type(value).__name__} was given')
        if not value == '':
            if not os.path.isfile(value):
                raise OSError('File ' + value + ' not found')
        self._filename = value

    @property
    def parameters(self):
        return self._parameters

    @parameters.setter
    def parameters(self, value):
        if not isinstance(value, str):
            raise TypeError(
                f'arg: parameters should be str. {type(value).__name__} was given')
        self._parameters = value

    @property
    def script(self):
        return self._script

    @script.setter
    def script(self, value):
        if not isinstance(value, str):
            raise TypeError(
                f'arg: script should be str. {type(value).__name__} was given')
        self._script = value

    @property
    def scriptLanguage(self):
        return self._scriptLanguage

    @scriptLanguage.setter
    def scriptLanguage(self, value):
        if not isinstance(value, ScriptLanguage):
            raise TypeError(
                f'arg: scriptLanguage should be ScriptLanguage. {type(value).__name__} was given')
        self._scriptLanguage = value

    @property
    def cacheKey(self):
        return self._cacheKey

    @cacheKey.setter
    def cacheKey(self, value):
        if not isinstance(value, bool):
            raise TypeError(
                f'arg: cacheKey should be bool. {type(value).__name__} was given')
        self._cacheKey = str(value).lower()

    def to_xml(self) -> str:
        """
        Set all parameters in xml and convert it to the string.
        :return: xml in string format
        """
        # default name and stuff setup
        element_root, xml_tree = super()._add_basics()
        for element in list(element_root):
            try:
                if element.attrib['name'] == 'cacheKey':
                    element.text = self.cacheKey
                elif element.attrib['name'] == 'filename':
                    element.text = self.filename
                elif element.attrib['name'] == 'parameters':
                    element.text = self.parameters
                elif element.attrib['name'] == 'script':
                    element.text = self.script
                elif element.attrib['name'] == 'scriptLanguage':
                    element.text = self.scriptLanguage.value
            except KeyError:
                logging.error('Unable to set xml parameters')

        return tree_to_str(xml_tree)