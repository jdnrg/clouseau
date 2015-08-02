from builtins import object

from abc import ABCMeta, abstractmethod
from future.utils import with_metaclass



class AbstractClient(with_metaclass(ABCMeta, object)):
    @abstractmethod
    def render(self,data):
        """
        Each instance of an AbstractClient must implement a render method, 
        which is called by Clouseau
        """
        raise Exception


