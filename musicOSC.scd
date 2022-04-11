s.boot;

(
SynthDef( \sin, { | amp = 0.01, freq = 333, trig = 0 |
    var env, sig;
	env = EnvGen.kr( Env.adsr(0.01, 0.1, 0), trig, doneAction: 0 );
	sig = SinOsc.ar( [ freq, freq * 0.999 ], 0.0, amp ) * env;
    Out.ar( [ 0 ], sig * 0.6 );
}).add;

SynthDef( \tri, { | amp = 0.01, freq = 333, trig = 0 |
    var env, sig;
	env = EnvGen.kr( Env.adsr(0.01, 0.1, 0), trig, doneAction: 0 );
	sig = LFTri.ar( [ freq, freq * 0.999 ], 0.0, amp ) * env;
    Out.ar( [ 0 ], sig * 0.6 );
}).add;

h = Synth( \sin, [ \amp, 0.4 ] );
i = Synth( \tri, [ \amp, 0.4 ] );
j = h;

x = OSCFunc( { | msg, time, addr, port |
    var pyFreq;
	// [msg, time, addr, port].postln;
	pyFreq = msg[1].asString;
	( "freq is " + pyFreq ).postln;
	j.set( \trig, 1, \freq, pyFreq.namecps );
	j.set( \trig, 0, \freq, pyFreq.namecps );
}, "/test", recvPort: 57120 );

y = OSCFunc( { | msg, time, addr, port |
    var ins;
	ins = msg[1].asString;
	( "ins is " + ins ).postln;
	j = i;
}, "/test2", recvPort: 57120 );


z = OSCFunc( { | msg, time, addr, port |
    var ins;
	ins = msg[1].asString;
	// ( "ins is " + ins ).postln;
	j = h;
}, "/test3", recvPort: 57120 );
)
