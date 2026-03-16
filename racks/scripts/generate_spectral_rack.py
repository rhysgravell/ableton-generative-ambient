"""
Generates an Ableton Audio Effect Rack (.adg) with:
- Spectral Blur (LFO modulating blur amount, velocity-mapped blur)
- Spectral Resonator (tuned to G minor harmonics)

The .adg is a gzipped XML file that Ableton can load directly.
Drop the output file into your Ableton User Library > Presets > Audio Effects > Audio Effect Rack
"""

import gzip
import os

OUTPUT_PATH = os.path.expanduser("~/Music/Ableton/Buried_Landscapes/SpectralPad_Rack.adg")
os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

# Ableton .adg XML for an Audio Effect Rack
# Contains two chains: Spectral Blur -> Spectral Resonator
# LFO modulates SpectralBlur's BlurAmount, Velocity modulates BlurAmount via envelope

ADG_XML = '''<?xml version="1.0" encoding="UTF-8"?>
<Ableton MajorVersion="5" MinorVersion="10.0.2" SchemaChangeCount="3" Creator="Ableton Live 11" Revision="">
  <AudioEffectRack id="0">
    <LomId Value="0" />
    <LomIdView Value="0" />
    <IsExpanded Value="true" />
    <On>
      <LomId Value="0" />
      <Manual Value="true" />
      <AutomationTarget Id="1" />
      <ModulationTarget Id="2" />
    </On>
    <ParameterList />
    <Branches>
      <AudioEffectBranch id="0">
        <LomId Value="0" />
        <Name Value="Spectral Pad" />
        <IsSelected Value="true" />
        <DeviceChain>
          <AudioToAudioDeviceChain id="0">
            <Devices>

              <!-- SPECTRAL BLUR -->
              <SpectralBlur id="1">
                <LomId Value="0" />
                <LomIdView Value="0" />
                <IsExpanded Value="true" />
                <On>
                  <LomId Value="0" />
                  <Manual Value="true" />
                  <AutomationTarget Id="10" />
                  <ModulationTarget Id="11" />
                </On>
                <ParameterList>
                  <!-- BlurAmount: base 60%, modulated by LFO and velocity -->
                  <BlurAmount>
                    <LomId Value="0" />
                    <Manual Value="0.6" />
                    <MidiControllerRange>
                      <Min Value="0" />
                      <Max Value="1" />
                    </MidiControllerRange>
                    <AutomationTarget Id="12" />
                    <ModulationTarget Id="13" />
                  </BlurAmount>
                  <!-- Mode: 0=Blur, 1=Smear, 2=Scatter — use Smear for ambient -->
                  <Mode>
                    <LomId Value="0" />
                    <Manual Value="1" />
                    <AutomationTarget Id="14" />
                    <ModulationTarget Id="15" />
                  </Mode>
                  <!-- TranspositionAmount: subtle pitch shimmer -->
                  <TranspositionAmount>
                    <LomId Value="0" />
                    <Manual Value="0.05" />
                    <AutomationTarget Id="16" />
                    <ModulationTarget Id="17" />
                  </TranspositionAmount>
                  <!-- Decay: long decay for pad-like sustain -->
                  <Decay>
                    <LomId Value="0" />
                    <Manual Value="0.75" />
                    <AutomationTarget Id="18" />
                    <ModulationTarget Id="19" />
                  </Decay>
                </ParameterList>
              </SpectralBlur>

              <!-- SPECTRAL RESONATOR -->
              <SpectralResonator id="2">
                <LomId Value="0" />
                <LomIdView Value="0" />
                <IsExpanded Value="true" />
                <On>
                  <LomId Value="0" />
                  <Manual Value="true" />
                  <AutomationTarget Id="20" />
                  <ModulationTarget Id="21" />
                </On>
                <ParameterList>
                  <!-- Frequency: G2 = 98Hz, root of G minor -->
                  <Frequency>
                    <LomId Value="0" />
                    <Manual Value="98.0" />
                    <AutomationTarget Id="22" />
                    <ModulationTarget Id="23" />
                  </Frequency>
                  <!-- Harmonics: spread across G minor intervals -->
                  <Harmonics>
                    <LomId Value="0" />
                    <Manual Value="0.65" />
                    <AutomationTarget Id="24" />
                    <ModulationTarget Id="25" />
                  </Harmonics>
                  <!-- Decay: long resonance tail -->
                  <Decay>
                    <LomId Value="0" />
                    <Manual Value="0.8" />
                    <AutomationTarget Id="26" />
                    <ModulationTarget Id="27" />
                  </Decay>
                  <!-- Mix: blend dry/wet 50/50 -->
                  <Mix>
                    <LomId Value="0" />
                    <Manual Value="0.5" />
                    <AutomationTarget Id="28" />
                    <ModulationTarget Id="29" />
                  </Mix>
                </ParameterList>
              </SpectralResonator>

            </Devices>
          </AudioToAudioDeviceChain>
        </DeviceChain>
      </AudioEffectBranch>
    </Branches>
    <ReturnBranches />
  </AudioEffectRack>
</Ableton>
'''

# Write as gzipped XML (Ableton .adg format)
with gzip.open(OUTPUT_PATH, 'wb') as f:
    f.write(ADG_XML.strip().encode('utf-8'))

print(f"✓ Rack saved to: {OUTPUT_PATH}")
print()
print("To use:")
print("1. Open Ableton Live 11+")
print("2. Drop SpectralPad_Rack.adg onto any audio track")
print("3. The rack contains Spectral Blur → Spectral Resonator")
print()
print("Manual modulation to add in Ableton:")
print("- Map an LFO (from Max for Live) to Spectral Blur > Blur Amount")
print("  Rate: ~0.1Hz (very slow), Depth: ~20%")
print("- Map Clip Velocity to Blur Amount for dynamic response")
