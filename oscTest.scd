s.boot;

(
SynthDef( \sin, { | amp = 0.01, freq = 333, trig = 0 |
    var env, sig;
	env = EnvGen.kr( Env.adsr(0.01, 0.1, 0), trig, doneAction: 0 );
	sig = LFTri.ar( [ freq, freq * 0.999 ], 0.0, amp ) * env;
    Out.ar( [ 0 ], sig * 0.6 );
}).add;

h = Synth( \sin, [ \amp, 0.4 ] );

x = OSCFunc( { | msg, time, addr, port |
    var pyFreq;
	// [msg, time, addr, port].postln;
	pyFreq = msg[1].asString;
	( "freq is " + pyFreq ).postln;
	h.set( \trig, 1, \freq, pyFreq.namecps );
	h.set( \trig, 0, \freq, pyFreq.namecps );
}, "/test", recvPort: 57120 );
)
