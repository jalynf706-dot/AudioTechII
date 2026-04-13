/*
  ==============================================================================

    This file contains the basic framework code for a JUCE plugin editor.

  ==============================================================================
*/

#include "PluginProcessor.h"
#include "PluginEditor.h"

//==============================================================================
_2526Activity10AudioProcessorEditor::_2526Activity10AudioProcessorEditor (_2526Activity10AudioProcessor& p)
    : AudioProcessorEditor (&p), audioProcessor (p),
    freqAttach(audioProcessor.apvts, "FREQ", freqSlider),
    ampAttach(audioProcessor.apvts, "AMP", ampSlider)

{

    freqSlider.setSliderStyle(juce::Slider::Rotary);
    freqSlider.setTextBoxStyle(juce::Slider::TextBoxBelow, false, 60, 20);
    addAndMakeVisible(freqSlider);

    ampSlider.setSliderStyle(juce::Slider::Rotary);
    ampSlider.setTextBoxStyle(juce::Slider::TextBoxBelow, false, 60, 20);
    addAndMakeVisible(ampSlider);

    // Make sure that before the constructor has finished, you've set the
    // editor's size to whatever you need it to be.
    setSize (400, 300);
}

_2526Activity10AudioProcessorEditor::~_2526Activity10AudioProcessorEditor()
{
}

//==============================================================================
void _2526Activity10AudioProcessorEditor::paint (juce::Graphics& g)
{
    // (Our component is opaque, so we must completely fill the background with a solid colour)
    g.fillAll (getLookAndFeel().findColour (juce::ResizableWindow::backgroundColourId));

    g.setColour (juce::Colours::white);
    g.setFont (juce::FontOptions (15.0f));
    g.drawFittedText ("Activity 10 Enveloped Sine Wave!", getLocalBounds(), juce::Justification::centred, 1);
}

void _2526Activity10AudioProcessorEditor::resized()
{
    // This is generally where you'll want to lay out the positions of any
    // subcomponents in your editor..

    freqSlider.setBounds(50, 60, 120, 120);
    ampSlider.setBounds(230, 60, 120, 120);

}
