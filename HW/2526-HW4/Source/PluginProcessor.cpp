/*
  ==============================================================================

    This file contains the basic framework code for a JUCE plugin processor.

  ==============================================================================
*/

#include "PluginProcessor.h"
#include "PluginEditor.h"

//==============================================================================
_2526HW4AudioProcessor::_2526HW4AudioProcessor()
#ifndef JucePlugin_PreferredChannelConfigurations
    : AudioProcessor (BusesProperties()
                    #if ! JucePlugin_IsMidiEffect
                     #if ! JucePlugin_IsSynth
                      .withInput  ("Input",  juce::AudioChannelSet::stereo(), true)
                     #endif
                      .withOutput ("Output", juce::AudioChannelSet::stereo(), true)
                    #endif
                      ),
      parameters (*this, nullptr, "PARAMETERS",
      {
          std::make_unique<juce::AudioParameterFloat>(
              "delayTime",
              "Delay Time",
              juce::NormalisableRange<float>(0.01f, (float)maxDelaySec),
              0.5f),

          std::make_unique<juce::AudioParameterFloat>(
              "wetMix",
              "Wet Mix",
              0.0f,
              1.0f,
              0.5f),

          std::make_unique<juce::AudioParameterFloat>(
              "feedback",
              "Feedback",
              0.0f,
              0.95f,
              0.2f)
      })
#endif
{
    delayTimeParam = (juce::AudioParameterFloat*) parameters.getParameter("delayTime");
    wetMixParam    = (juce::AudioParameterFloat*) parameters.getParameter("wetMix");
    feedbackParam  = (juce::AudioParameterFloat*) parameters.getParameter("feedback");
}

_2526HW4AudioProcessor::~_2526HW4AudioProcessor()
{
}

//==============================================================================
const juce::String _2526HW4AudioProcessor::getName() const
{
    return JucePlugin_Name;
}

bool _2526HW4AudioProcessor::acceptsMidi() const
{
   #if JucePlugin_WantsMidiInput
    return true;
   #else
    return false;
   #endif
}

bool _2526HW4AudioProcessor::producesMidi() const
{
   #if JucePlugin_ProducesMidiOutput
    return true;
   #else
    return false;
   #endif
}

bool _2526HW4AudioProcessor::isMidiEffect() const
{
   #if JucePlugin_IsMidiEffect
    return true;
   #else
    return false;
   #endif
}

double _2526HW4AudioProcessor::getTailLengthSeconds() const
{
    return 0.0;
}

int _2526HW4AudioProcessor::getNumPrograms()
{
    return 1;   // NB: some hosts don't cope very well if you tell them there are 0 programs,
                // so this should be at least 1, even if you're not really implementing programs.
}

int _2526HW4AudioProcessor::getCurrentProgram()
{
    return 0;
}

void _2526HW4AudioProcessor::setCurrentProgram (int index)
{
}

const juce::String _2526HW4AudioProcessor::getProgramName (int index)
{
    return {};
}

void _2526HW4AudioProcessor::changeProgramName (int index, const juce::String& newName)
{
}

//==============================================================================
void _2526HW4AudioProcessor::prepareToPlay (double sampleRate, int samplesPerBlock)
{
    // call your initializing functions and set variables here!

    int maxDelaySamples = (int)(maxDelaySec * sampleRate);
    delay.prepare(sampleRate, maxDelaySamples, getTotalNumInputChannels());

    float frequency = 440.0f;
    phaseIncrement = juce::MathConstants<float>::twoPi * frequency / (float)sampleRate;


}

void _2526HW4AudioProcessor::releaseResources()
{
    // When playback stops, you can use this as an opportunity to free up any
    // spare memory, etc.
}

#ifndef JucePlugin_PreferredChannelConfigurations
bool _2526HW4AudioProcessor::isBusesLayoutSupported (const BusesLayout& layouts) const
{
  #if JucePlugin_IsMidiEffect
    juce::ignoreUnused (layouts);
    return true;
  #else
    // This is the place where you check if the layout is supported.
    // In this template code we only support mono or stereo.
    // Some plugin hosts, such as certain GarageBand versions, will only
    // load plugins that support stereo bus layouts.
    if (layouts.getMainOutputChannelSet() != juce::AudioChannelSet::mono()
     && layouts.getMainOutputChannelSet() != juce::AudioChannelSet::stereo())
        return false;

    // This checks if the input layout matches the output layout
   #if ! JucePlugin_IsSynth
    if (layouts.getMainOutputChannelSet() != layouts.getMainInputChannelSet())
        return false;
   #endif

    return true;
  #endif
}
#endif

void _2526HW4AudioProcessor::processBlock (juce::AudioBuffer<float>& buffer, juce::MidiBuffer& midiMessages)
{
    juce::ScopedNoDenormals noDenormals;
    auto totalNumInputChannels  = getTotalNumInputChannels();
    auto totalNumOutputChannels = getTotalNumOutputChannels();
    
    int numSamples = buffer.getNumSamples();
    delay.setDelayTime(delayTimeParam->get());
    delay.setWetMix(wetMixParam->get());
    delay.setFeedbackAmt(feedbackParam->get());

    for (auto i = totalNumInputChannels; i < totalNumOutputChannels; ++i)
        buffer.clear (i, 0, numSamples);

    for (int channel = 0; channel < totalNumInputChannels; ++channel)
    {
        auto* channelData = buffer.getWritePointer (channel);

        // ---- TEST AUDIO GENERATION (float only) ----
        for (int i = 0; i < numSamples; ++i)
        {
            channelData[i] = std::sin(phase) * 0.25f;

            phase += phaseIncrement;
            if (phase >= juce::MathConstants<float>::twoPi)
                phase -= juce::MathConstants<float>::twoPi;
        }


        for (int i = 0; i < numSamples; ++i)
        {
            // your delay function is called below. Do not change
            channelData[i] = delay.processSample(channelData[i], channel);

        }
    }
}

//==============================================================================
bool _2526HW4AudioProcessor::hasEditor() const
{
    return false; // (change this to false if you choose to not supply an editor)
}

juce::AudioProcessorEditor* _2526HW4AudioProcessor::createEditor()
{
    return new _2526HW4AudioProcessorEditor (*this);
}

//==============================================================================
void _2526HW4AudioProcessor::getStateInformation (juce::MemoryBlock& destData)
{
    // You should use this method to store your parameters in the memory block.
    // You could do that either as raw data, or use the XML or ValueTree classes
    // as intermediaries to make it easy to save and load complex data.
}

void _2526HW4AudioProcessor::setStateInformation (const void* data, int sizeInBytes)
{
    // You should use this method to restore your parameters from this memory block,
    // whose contents will have been created by the getStateInformation() call.
}

//==============================================================================
// This creates new instances of the plugin..
juce::AudioProcessor* JUCE_CALLTYPE createPluginFilter()
{
    return new _2526HW4AudioProcessor();
}
