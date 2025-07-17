import mido

# Configuration
INPUT_PORT = 'DDJ-FLX6'                      # Exact input port name
OUTPUT_PORT = 'IAC Driver Python_MIDI_Out'  # Exact output port name
MERGEFX_NOTE = 46
ALT_NOTE = 49
CHANNELS = [4, 5]  # MIDI channels to support

# Initialize toggle states per channel
toggle_states = {ch: True for ch in CHANNELS}

def main():
    inport = mido.open_input(INPUT_PORT)
    outport = mido.open_output(OUTPUT_PORT)

    try:
        for msg in inport:
            if (
                msg.type == 'note_on' and
                msg.note == MERGEFX_NOTE and
                msg.channel in CHANNELS
            ):
                ch = msg.channel
                toggle_state = toggle_states[ch]

                # Determine output note based on toggle state
                out_note = ALT_NOTE if toggle_state else MERGEFX_NOTE

                # On release, flip toggle state; on press, keep it
                if msg.velocity == 0:
                    toggle_states[ch] = not toggle_state
                    velocity = 0
                elif msg.velocity == 127:
                    velocity = 127
                else:
                    continue  # ignore other velocities

                out_msg = mido.Message('note_on', note=out_note, velocity=velocity, channel=ch)
                outport.send(out_msg)

    except KeyboardInterrupt:
        # Exit cleanly on Ctrl+C
        pass
    finally:
        inport.close()
        outport.close()

if __name__ == "__main__":
    main()
