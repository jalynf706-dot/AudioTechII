/*
  ==============================================================================

    Delay.cpp
 
    This code contains the implementation needed for a simple feedback delay.

  ==============================================================================
*/

#include "Delay.h"


void Delay::prepare(double samplingRate, int maxDelay, int numChannels)
{
    sampleRate = samplingRate;
    maxDelayInSamples = maxDelay;
    delayBufferSize = maxDelayInSamples + 1;

    delayBuffer.setSize(numChannels, delayBufferSize);
    delayBuffer.clear();

    writeHeads.clear();
    writeHeads.resize(numChannels, 0);

    smoothedDelay.reset(sampleRate, 0.05f);
    smoothedDelay.setCurrentAndTargetValue(0.0f);
}

void Delay::setMaxDelayInSamples(int maxDelay)
{
    maxDelayInSamples = maxDelay;
}

int Delay::getMaxDelayInSamples()
{
    return maxDelayInSamples;
}

void Delay::setDelayTime(float delaySecondsIn)
{
    delaySeconds = delaySecondsIn;

    int newDelaySamples = (int)(delaySeconds * sampleRate);
    newDelaySamples = juce::jlimit(0, maxDelayInSamples, newDelaySamples);

    smoothedDelay.setTargetValue((float)newDelaySamples);
}

void Delay::setWetMix(float wetAmount)
{
    mix = juce::jlimit(0.0f, 1.0f, wetAmount);
}

void Delay::setFeedbackAmt(float feedbackAmt)
{
    feedback = juce::jlimit(0.0f, 0.95f, feedbackAmt);
}

// this is called in the ProcessBlock as we iterate over each channel's buffer
float Delay::processSample(float inputSample, int channel)
{
    int writeIndex = writeHeads[channel];
    int delaySamples = (int)smoothedDelay.getNextValue();
    int readIndex = writeIndex - delaySamples;

    if (readIndex < 0)
        readIndex += delayBufferSize;

    float delayedSample = delayBuffer.getSample(channel, readIndex);

    float bufferInput = inputSample + delayedSample * feedback;
    delayBuffer.setSample(channel, writeIndex, bufferInput);

    writeHeads[channel]++;
    if (writeHeads[channel] >= delayBufferSize)
        writeHeads[channel] = 0;

    return inputSample * (1.0f - mix) + delayedSample * mix;
}
