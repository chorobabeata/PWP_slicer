import os
import unittest
import vtk, qt, ctk, slicer
from slicer.ScriptedLoadableModule import *
import logging

#
# ScrModule
#

class ScrModule(ScriptedLoadableModule):
  """Uses ScriptedLoadableModule base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def __init__(self, parent):
    ScriptedLoadableModule.__init__(self, parent)
    self.parent.title = "ScrModule" # TODO make this more human readable by adding spaces
    self.parent.categories = ["Examples"]
    self.parent.dependencies = []
    self.parent.contributors = ["John Doe (AnyWare Corp.)"] # replace with "Firstname Lastname (Organization)"
    self.parent.helpText = """
    This is an example of scripted loadable module bundled in an extension.
    It performs a simple thresholding on the input volume and optionally captures a screenshot.
    """
    self.parent.acknowledgementText = """
    This file was originally developed by Jean-Christophe Fillion-Robin, Kitware Inc.
    and Steve Pieper, Isomics, Inc. and was partially funded by NIH grant 3P41RR013218-12S1.
""" # replace with organization, grant and thanks.

#
# ScrModuleWidget
#

class ScrModuleWidget(ScriptedLoadableModuleWidget):
  """Uses ScriptedLoadableModuleWidget base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def setup(self):
    ScriptedLoadableModuleWidget.setup(self)

    # Instantiate and connect widgets ...
    
    
    #
    # Modele Area
    #
    modelsCollapsibleButton = ctk.ctkCollapsibleButton()
    modelsCollapsibleButton.text = "Models"
    self.layout.addWidget(modelsCollapsibleButton)
    
    modelsFormLayout = qt.QFormLayout(modelsCollapsibleButton)
    
    #
    # Modele Combo
    #
    
    self.modelsSelector = slicer.qMRMLNodeComboBox()
    self.modelsSelector.nodeTypes = ["vtkMRMLModelNode"]
    self.modelsSelector.selectNodeUponCreation = True
    self.modelsSelector.addEnabled = False
    self.modelsSelector.removeEnabled = True
    self.modelsSelector.noneEnabled = True
    self.modelsSelector.showHidden = False
    self.modelsSelector.showChildNodeTypes = False
    self.modelsSelector.setMRMLScene( slicer.mrmlScene )
    self.modelsSelector.setToolTip( "Pick the input to the algorithm." )
    modelsFormLayout.addRow("Input Model: ", self.modelsSelector)

    #
    # opacity value
    #
    self.modelOpacitySliderWidget = ctk.ctkSliderWidget()
    self.modelOpacitySliderWidget.singleStep = 0.1
    self.modelOpacitySliderWidget.minimum = 0
    self.modelOpacitySliderWidget.maximum = 100
    self.modelOpacitySliderWidget.value = 50
    self.modelOpacitySliderWidget.setToolTip("Set opacity value for computing the output image.")
    modelsFormLayout.addRow("Model opacity", self.modelOpacitySliderWidget)

    #
    # Show Button
    #
    self.showHideButton = qt.QPushButton("Show/Hide")
    self.showHideButton.toolTip = "Show/hide the model"
    self.showHideButton.enabled = True
    modelsFormLayout.addRow(self.showHideButton)


    # connections

    self.showHideButton.connect('clicked(bool)', self.onShowHideButton)
    self.modelOpacitySliderWidget.connect('valueChanged(double)', self.onSliderValueChanged)

    # Add vertical spacer
    self.layout.addStretch(1)

  def cleanup(self):
    pass

  def onShowHideButton(self):
    logic = ScrModuleLogic()
    logic.showHideModel(self.modelsSelector.currentNode())

  def onSliderValueChanged(self):
    logic = ScrModuleLogic()
    opacityValue = self.modelOpacitySliderWidget.value
    logic.changeOpacity(self.modelsSelector.currentNode(), opacityValue)

#
# ScrModuleLogic
#

class ScrModuleLogic(ScriptedLoadableModuleLogic):
  """This class should implement all the actual
  computation done by your module.  The interface
  should be such that other python code can import
  this class and make use of the functionality without
  requiring an instance of the Widget.
  Uses ScriptedLoadableModuleLogic base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """
  
  def isValidModelData(self, modelNode):
    """Validates if the model is empty
      """
    if not modelNode:
      logging.debug('isValidAllData failed: no model node defined')
      return False
    return True


  def changeOpacity(self, model, opacityVal):
    if not self.isValidModelData( model):
      slicer.util.errorDisplay('Wrong input model')
      return False
    n = model.GetDisplayNode()
    n.SetOpacity(opacityVal/100)
    return True

  def showHideModel(self, model):
    if not self.isValidModelData( model):
      slicer.util.errorDisplay('Wrong input model')
      return False
    n = model.GetDisplayNode()
    v = n.GetVisibility()
    if (v==1):
      n.SetVisibility(0)
    else:
      n.SetVisibility(1)


class ScrModuleTest(ScriptedLoadableModuleTest):
  """
  This is the test case for your scripted module.
  Uses ScriptedLoadableModuleTest base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def setUp(self):
    """ Do whatever is needed to reset the state - typically a scene clear will be enough.
    """
    slicer.mrmlScene.Clear(0)

  def runTest(self):
    """Run as few or as many tests as needed here.
    """
    self.setUp()
    self.test_ScrModule1()

  def test_ScrModule1(self):
    """ Ideally you should have several levels of tests.  At the lowest level
    tests should exercise the functionality of the logic with different inputs
    (both valid and invalid).  At higher levels your tests should emulate the
    way the user would interact with your code and confirm that it still works
    the way you intended.
    One of the most important features of the tests is that it should alert other
    developers when their changes will have an impact on the behavior of your
    module.  For example, if a developer removes a feature that you depend on,
    your test should break so they know that the feature is needed.
    """

    self.delayDisplay("Starting the test")
    #
    # first, get some data
    #
    import urllib
    downloads = (
        ('http://slicer.kitware.com/midas3/download?items=5767', 'FA.nrrd', slicer.util.loadVolume),
        )

    for url,name,loader in downloads:
      filePath = slicer.app.temporaryPath + '/' + name
      if not os.path.exists(filePath) or os.stat(filePath).st_size == 0:
        logging.info('Requesting download %s from %s...\n' % (name, url))
        urllib.urlretrieve(url, filePath)
      if loader:
        logging.info('Loading %s...' % (name,))
        loader(filePath)
    self.delayDisplay('Finished with download and loading')

    volumeNode = slicer.util.getNode(pattern="FA")
    logic = ScrModuleLogic()
    self.assertTrue( logic.hasImageData(volumeNode) )
    self.delayDisplay('Test passed!')
