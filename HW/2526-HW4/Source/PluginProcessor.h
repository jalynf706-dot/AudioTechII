/*
  ==============================================================================

    This file contains the basic framework code for a JUCE plugin processor.

  ==============================================================================
*/

#pragma once

#include <JuceHeader.h>
#include "Delay.h"

//==============================================================================
/**
*/
class _2526HW4AudioProcessor  : public juce::AudioProcessor
{
public:
    //==============================================================================
    _2526HW4AudioProcessor();
    ~_2526HW4AudioProcessor() override;

    //==============================================================================
    void prepareToPlay (double sampleRate, int samplesPerBlock) override;
    void releaseResources() override;

   #ifndef JucePlugin_PreferredChannelConfigurations
    bool isBusesLayoutSupported (const BusesLayout& layouts) const override;
   #endif

    void processBlock (juce::AudioBuffer<float>&, juce::MidiBuffer&) override;

    //==============================================================================
    juce::AudioProcessorEditor* createEditor() override;
    bool hasEditor() const override;

    //==============================================================================
    const juce::String getName() const override;

    bool acceptsMidi() const override;
    bool producesMidi() const override;
    bool isMidiEffect() const override;
    double getTailLengthSeconds() const override;

    //==============================================================================
    int getNumPrograms() override;
    int getCurrentProgram() override;
    void setCurrentProgram (int index) override;
    const juce::String getProgramName (int index) override;
    void changeProgramName (int index, const juce::String& newName) override;

    //==============================================================================
    void getStateInformation (juce::MemoryBlock& destData) override;
    void setStateInformation (const void* data, int sizeInBytes) override;


private:
    //==============================================================================
    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR (_2526HW4AudioProcessor)

    Delay delay;
    const int maxDelaySec = 5;

    float phase = 0.0f;
    float phaseIncrement = 0.0f;

    juce::AudioProcessorValueTreeState apvts;
    juce::AudioParameterFloat* delayTimeParam = nullptr;
    juce::AudioParameterFloat* wetMixParam = nullptr;
    juce::AudioParameterFloat* feedbackParam = nullptr;
};
