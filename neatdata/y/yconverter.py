import numpy as np
from neatdata.numpyhelper.numpyhelper import *

class YConverter:

    def __init__(self):
        self._trainYMappingsStrToNum, self._trainYMappingsNumToStr = None, None
        self._trainYListOfValidInputs = None
        self._stringWasPassedToMapping = None
        self._setYMappingsWasRun = False

    def setYMappings(self, y):
        self._trainYMappingsStrToNum, self._trainYMappingsNumToStr = {'NotFound': -99}, {-99: 'NotFound'}
        self._trainYListOfValidInputs = [-99]
        self._setYMappingsWasRun = True
        self._stringWasPassedToMapping = True if isStringType(y) else False
        if not self._stringWasPassedToMapping:
            y[y == np.inf] = -99
            y[y == -np.inf] = -99
            for value in np.unique(y):
                if value != None and not np.isnan(value):
                    self._trainYListOfValidInputs.append(value)
            return
        i = 0
        for value in np.unique(y):
            if value != None and value.strip() != "":
                self._trainYMappingsStrToNum[value] = i
                self._trainYMappingsNumToStr[i] = value
                i = i + 1

    def convertYToNumbersForModeling(self, y):
        y = castAsNumpy(y)
        yIsStringType = isStringType(y)
        self._raiseExceptionsForConvertYToNumbersForModeling(yIsStringType)
        if yIsStringType and self._stringWasPassedToMapping:
            return self._convertStringToNumber(y)
        elif not yIsStringType and self._stringWasPassedToMapping:
            return self._convertNumberToNumberWithMapping(y)
        elif not yIsStringType and not self._stringWasPassedToMapping:
            return self._convertNumberToNumberWithList(y)
        else:
            raise Exception('Error: Impossible event.')

    def _raiseExceptionsForConvertYToNumbersForModeling(self, yIsStringType):
        if not self._setYMappingsWasRun: raise Exception('Error: run setYMappings before convertToNumber')
        if not self._stringWasPassedToMapping and yIsStringType: raise Exception('Error: Y was not string during setYMappings, therefore Y must be a number.')

    def _convertStringToNumber(self, y):
        y = self._prepareStringForMapping(y)
        return np.vectorize(self._trainYMappingsStrToNum.get)(y)

    def _prepareStringForMapping(self, y):
        for i in range(len(y)):
            if y[i] == None or y[i] not in self._trainYMappingsStrToNum.keys():
                y[i] = 'NotFound'
        return y

    def _convertNumberToNumberWithMapping(self, y):
        return self._prepareNumberForMapping(y)

    def _prepareNumberForMapping(self, y):
        y[y == np.inf] = -99
        y[y == -np.inf] = -99
        for i in range(len(y)):
            if np.isnan(y[i]) or y[i] not in self._trainYMappingsStrToNum.values():
                y[i] = -99
        return y

    def _convertNumberToNumberWithList(self, y):
        y[y == np.inf] = -99
        y[y == -np.inf] = -99
        for i in range(len(y)):
            if np.isnan(y[i]) or y[i] not in self._trainYListOfValidInputs:
                y[i] = -99
        return y

    def convertYToStringsOrNumbersForPresentation(self, y):
        y = castAsNumpy(y)
        yIsStringType = isStringType(y)
        self._raiseExceptionsForConvertYToStringsOrNumbersForPresentation(yIsStringType)
        if yIsStringType and self._stringWasPassedToMapping:
            return self._convertStringToString(y)
        elif not yIsStringType and self._stringWasPassedToMapping:
            return self._convertNumberToString(y)
        elif not yIsStringType and not self._stringWasPassedToMapping:
            return y
        else:
            raise Exception('Error: Impossible event.')

    def _raiseExceptionsForConvertYToStringsOrNumbersForPresentation(self, yIsStringType):
        if not self._setYMappingsWasRun: raise Exception('Error: run setYMappings before convertToString')
        if not self._stringWasPassedToMapping and yIsStringType: raise Exception('Error: Y was not string during setYMappings, so converting from string to number is not possible..')

    def _convertStringToString(self, y):
        return self._prepareStringForMapping(y)

    def _convertNumberToString(self, y):
        y = self._prepareNumberForMapping(y)
        return np.vectorize(self._trainYMappingsNumToStr.get)(y)
