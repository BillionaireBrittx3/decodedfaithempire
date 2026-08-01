import json, os
# Batch 1: devotions 1-12 (Part One). Straight quotes; apply.py adds typographic curls.
B = {
"1": {"teaching": [
"Every man keeps a private scoreboard. You may not admit it exists, but you feel it every time another man's life looks further along than yours—his title, his timing, his marriage, the ease he seems to move through the world with. The scoreboard is loud, and it lies.",
"Here is what comparison rarely tells you: you are measuring your unedited life against someone else's summary. You see his result, not his cost. You see the house, not the decade of quiet work behind it. And while you stare at his highlight, you quietly abandon your own next step—the ordinary, unglamorous move that actually belongs to you today.",
"There is a promise in Scripture for the man who feels behind. The steps of a man who genuinely wants to walk with God are being ordered by God Himself, and a stumble along the way is not a disqualification. Read that slowly. He is guiding your steps, not clocking your pace. Your speed is not your verdict.",
"So the work today is not to catch up. It is to get honest about which race you are even running. Some of your hurry is God-given ambition worth honoring. Some of it is fear wearing a nice suit. Ask Him to show you the difference, because a man who chases someone else's timeline usually arrives as someone he no longer respects.",
"You are not late. You are in process, which is the only place real character has ever been built. Take the next faithful step—the small one you keep skipping—and let God carry the distance."
], "prayer": [
"Father, You see the scoreboard I pretend I'm not keeping. You know the names I quietly measure myself against and the ache of feeling passed over. I'm bringing all of it into the open with You instead of carrying it alone.",
"Forgive me for treating my worth like a race I'm losing. Forgive me for despising the ordinary road You've actually given me while I stare at someone else's. Quiet the comparison long enough for me to hear Your voice again.",
"Teach me to trust the steps You are ordering, even the slow ones I don't understand. Where I've rushed ahead of You out of fear, bring me back. Where I've stalled out and stopped moving, give me courage for the next step.",
"Help me measure my life by faithfulness instead of speed. Let me celebrate other men without losing myself in the comparison. And let me believe, today, that being in process is not the same as being forgotten by You.",
"I don't need to arrive by a certain age to be a man You are proud of. I only need to keep walking with You, one honest step at a time.",
"I trust You with the timing. Amen."
]},
"2": {"teaching": [
"There is a particular kind of exhaustion that has learned to smile. You answer the texts. You show up to work. You tell people you're good, and you're not entirely lying—you are functioning. But functioning and flourishing are not the same thing, and somewhere underneath the routine, your heart has been trying to get your attention.",
"Men become experts at this. We can carry a heavy internal life into a completely normal-looking day and let no one see the weight of it. The real danger is not that you're hiding it from others. It's that, after long enough, you start hiding it from yourself, until the numbness begins to feel like peace and the silence begins to feel like strength.",
"But God does not require you to be composed before He'll come close. He stays nearest to the ones whose hearts are quietly breaking, not the ones who perform the best. He is not standing on the far side of your recovery, waiting for you to arrive. He is already in the room with the part of you that is struggling right now.",
"Integrity is not mainly about being honest in public. It's about closing the gap between the man everyone sees and the man you actually are. That gap does not close by trying harder to look fine. It begins to close the moment you let one true sentence out into the open.",
"You don't have to announce everything to everyone. But a struggle kept completely sealed will keep running your life from the dark. Bring it into the light—first to God, who already knows, and then to one person who has earned the truth."
], "prayer": [
"Lord, I'm tired of saying I'm fine. You already know the truth underneath the routine—the weight I carry into ordinary days and never set down. I'm done pretending it isn't there.",
"I confess that I've hidden my struggle so well I've nearly fooled myself. I've called numbness peace and silence strength. Meet me in the place I've kept sealed off, even from my own eyes.",
"Thank You that You don't wait for me to be composed before You draw near. Thank You that You stay closest to a breaking heart. I need that nearness far more than I need to look okay.",
"Give me the courage to say one true sentence out loud—to You, and then to someone safe. Close the distance between the man people see and the man I actually am when no one is watching.",
"I don't want to keep managing this alone in the dark. Bring it into Your light, and let honesty be the first step toward healing.",
"I'm trusting You with what I've hidden. Amen."
]},
"3": {"teaching": [
"I once knew a man who could fix anything—engines, roofs, other people's problems—and who never once, in forty years, asked for help. Everyone admired him. Almost no one truly knew him. When his health finally broke, he had a hundred acquaintances and no one to sit with him, because he had spent a lifetime teaching everyone that he never needed a thing.",
"Somewhere we picked up the idea that a strong man is a sealed man. Say less. Need nothing. Handle it alone. But silence isn't strength; it's strength with no exit—pressure with nowhere to go. And pressure that never gets spoken doesn't quietly disappear. It leaks, and it usually leaks onto the people you love most.",
"God never designed you to carry your weight solo. He tells us to help carry one another's burdens, which means He assumes you will have burdens too heavy to lift by yourself, and that letting a brother get under the load with you is obedience, not failure.",
"Real courage isn't refusing to speak. It's being willing to say, out loud, to another man, that something is hard and you could use help. That one sentence costs more than most of the tough things you do all week. It is also the doorway to nearly everything you actually need.",
"You will not look weak. You will look like a man secure enough to stop performing. The people worth keeping don't respect the mask anyway. They respect the man brave enough to take it off. Strength that can be shared outlasts strength that only knows how to stand alone."
], "prayer": [
"God, I've believed for a long time that staying silent was the same thing as being strong. I'm starting to see what that has cost me. I don't want to be admired from a distance and known by no one.",
"You built me for brotherhood, not isolation. Forgive me for the pride that keeps calling it independence. Forgive me for making everyone believe I never need a single thing.",
"Give me the courage to say the hard sentence—to name what's heavy and let another man help me carry it. Send me one person I can trust, and make me willing to be that kind of man for someone else.",
"Teach me that needing help is not weakness but wisdom, and that a burden spoken out loud is already lighter than a burden hidden in silence.",
"Where I've quietly leaked my pressure onto the people I love, lead me to make it right. Where I've gone silent, help me open the door.",
"Give me the courage to be known. Amen."
]},
"4": {"teaching": [
"Can a memory be a warden? Ask the man who has technically been forgiven but still serves a sentence every night, when the lights go off and the old scene starts playing again. He believes in grace. He preaches it to other people. He just cannot seem to receive it for the one thing he cannot undo.",
"Here is a distinction that can set you free: conviction and condemnation are not the same voice. Conviction is specific and hopeful—it names the wrong and points toward repair. Condemnation is vague and crushing—it names you, not the act, and offers no way forward. One is a Father restoring a son. The other is a prosecutor with no jurisdiction over you anymore.",
"Because if you belong to Christ, the sentence has already been served. There is no condemnation left hanging over you—not a suspended one, not a probationary one. The case is closed. The gavel came down at the cross, and the verdict that came back was mercy.",
"That does not mean you skip repair. Grace and responsibility are partners, not rivals. Where your past still owes someone an honest apology or a changed pattern, go make it right. But making it right is a different thing from making yourself pay forever. Jesus already covered the part you could never repay.",
"So take the memory out of the shadows and set it in front of God. Let Him show you what to learn from it, what still needs mending, and what you are finally allowed to put down. You were never meant to serve as your own judge and your own jailer."
], "prayer": [
"Jesus, You know the memory I keep replaying—the one that still speaks louder than Your grace. I've believed the accusation more than I've believed You. I'm bringing it to You again tonight instead of hiding with it.",
"Thank You that there is no condemnation left for me, because You already carried it. The case is closed. Help me stop reopening a verdict You settled once and for all at the cross.",
"Teach me to tell the difference between Your conviction, which heals, and the shame that only crushes. Where I still owe someone repair, give me the humility to go and make it right.",
"But where I've only been punishing myself, set me free. I don't have to keep paying for what You already paid in full. Let grace reach the exact place I've kept off-limits to it.",
"Quiet the accuser's voice with the truth of who I am to You—forgiven, not on probation; a son, not a prisoner.",
"Let me rest tonight like a man who is no longer on trial. Amen."
]},
"5": {"teaching": [
"There's a strange moment that happens to a lot of men in the middle of a long, hard season. You catch your own reflection—in a window, a video call, a photo someone tagged—and for half a second you think, who is that? Not older, exactly. Just someone you've slowly lost track of.",
"Survival mode does that to a man. When you spend months, or years, just absorbing hits and keeping things running, you gradually disconnect from the person underneath the coping. The laughter thins out. The curiosity goes quiet. You're still here, still producing, still dependable—but the you-ness of you feels like it's watching from somewhere far off.",
"Here is the truth the Bible speaks over a man in Christ: you are not the sum of your worst season. Life in Christ makes something genuinely new, and the old version does not get the final word on who you are. The man you're afraid you've permanently become is not your ending.",
"Recovering yourself is rarely a lightning bolt. It's usually a re-introduction—small, deliberate returns to the things that once made you feel awake. A practice. A friendship. A responsibility carried with joy again instead of dread. God tends to restore a man the same patient way He forms him: one honest step at a time.",
"You don't have to resurrect the old you. You get to keep becoming the man God is actually making—steadier, deeper, and more himself than the version you're grieving. Endurance isn't only surviving the season. It's still being here, and still becoming, long after the first rush of motivation has burned off."
], "prayer": [
"God, somewhere in all the surviving, I've lost track of myself. I look up and don't fully recognize the man I've become. You still do. You have never once lost sight of me, even when I lost sight of me.",
"Thank You that in Christ I am not the sum of my hardest season. Thank You that the old version doesn't get the last word, and that You are in the business of making things new—even here, especially here.",
"Reintroduce me to the man You created me to be. Bring back the laughter, the curiosity, the steadiness I've missed. Show me the small returns that lead me home to myself in You, one quality at a time.",
"Give me endurance for the slow work of restoration—the strength to keep showing up after the first burst of motivation fades and the real forming begins.",
"I don't need to resurrect who I used to be. I want to become who You are patiently making me.",
"Make me new, and make me whole. Amen."
]},
"6": {"teaching": [
"Counselors have a phrase worth knowing: anger is a secondary emotion. It's the bodyguard that shows up first so you never have to feel the more vulnerable thing standing behind it—the hurt, the fear, the grief, the helplessness. Anger feels powerful, which is exactly why we so often prefer it to whatever it's covering for.",
"So when irritation keeps leaking into ordinary conversations—snapping at your kid over nothing, tension in your jaw before a word is even spoken—it's usually a messenger, not the message. Something underneath is asking to be heard, and it will keep raising its voice until you finally stop and listen to it.",
"Scripture hands the wise man a rhythm: quick to listen, slow to speak, slow to anger. Notice the order. Listening comes first—and some of that listening is inward. Your anger rarely produces the kind of life God is after, but it can point you toward what needs attention, if you'll slow down long enough to read it honestly.",
"Humility is what makes this possible. It takes a secure man to pause mid-reaction and ask a real question instead of defending his flare-up. Not who made me feel this way, but what is this actually about? That single question has defused more conflicts than any comeback ever has.",
"You are not a bad man for feeling anger. You're a growing one for finally getting curious about it. Get underneath the reaction, and you'll usually find something God wants to heal, not just something He wants you to white-knuckle into silence."
], "prayer": [
"Father, I've been irritable in ways that don't quite add up, and I don't fully understand why. You see what's underneath the anger even when I can't. I'm asking You to show me what my reactions are really about.",
"Help me be slow enough to listen—first to the people around me, and then to what my own flares are trying to tell me. I don't want to keep leaking pressure onto the ones I love most.",
"When the reaction rises, hold me for one honest second and let me ask what I'm really protecting, grieving, fearing, or needing. Meet me in that tender place instead of the armored one I usually retreat to.",
"Give me the humility to own my part without excuse, to apologize quickly, and to change direction without feeling like I've lost myself in the process.",
"Heal the thing beneath the anger. I would rather be honest and whole than defended and hard.",
"Search me, and lead me. Amen."
]},
"7": {"teaching": [
"Every long walk with God includes stretches of weather that feel like nothing at all. You still pray. You still show up on Sunday. You still crack open the Bible. But the warmth is gone, and you start to wonder if something is wrong with your faith—or wrong with you.",
"Usually, nothing is broken. You're in a dry season, and dry seasons are normal in Scripture, not evidence of failure. Even the psalmist talked directly to his own downcast soul and told it, right in the middle of the numbness, to put its hope in God. He didn't wait until he felt it before he said it.",
"That's the counterintuitive part: feelings tend to follow faithfulness, not the other way around. If you wait to feel close to God before you'll seek Him, you may be waiting a long time. But the man who keeps the small practices during the dry stretch is the man whose heart eventually catches back up to his obedience.",
"So don't strain to manufacture an emotional high. Just stay in the room. Five honest minutes of prayer. One Psalm. A quiet walk where you say almost nothing at all. Numbness is not the absence of God; it's often the place where a man's faith learns to stand on what's true instead of on how he happens to feel.",
"Keep showing up. The fire you can't feel right now is still there under the ash, and God is patient enough, and faithful enough, to fan it back to warmth in His own good timing."
], "prayer": [
"Lord, my heart feels far away even while I'm doing the right things. I pray and read and show up, and it all feels like static. You are not fooled by the numbness, and You have not gone anywhere.",
"Like the psalmist, I'll say it before I feel it: I put my hope in You. Be my anchor in this flat, quiet stretch when nothing inside me seems to move.",
"Teach me to stay in the room without forcing an emotion. Meet me in five honest minutes, in one Psalm, in a quiet walk. Let faithfulness lead the way and let my feelings follow in Your timing, not mine.",
"Thank You that dryness is not distance, and that You are just as near when I feel nothing as when I feel everything.",
"Fan the fire back to warmth beneath the ash. And until You do, keep me steady, present, and honest with You.",
"I'll keep showing up. Amen."
]},
"8": {"teaching": [
"You've made this promise before. Maybe more than once. And the shame of the repeat attempt is heavier than the shame of the original failure, because now there's a track record—and the track record whispers that you're simply the kind of man who doesn't follow through.",
"But here's what the science of change quietly confirms and what grace says out loud: almost no one changes on the first attempt. Lasting change is a spiral, not a switch. You circle back to the same lesson at a slightly higher level each time around. Starting over isn't proof that you failed. It's how the process has always actually worked.",
"The reason most promises collapse isn't weak willpower—it's vague design. I'll do better has no handles to grab. I'll get up when the first alarm rings and read one Psalm before I touch my phone does. Willpower is unreliable fuel. Structure is what carries a man forward on the days motivation simply doesn't show up.",
"And here is the mercy underneath the method: God's compassion does not wear thin with your repeat attempts. It is new every single morning—not a limited supply you've been slowly draining, but a fresh delivery you get to receive again today, no matter how yesterday ended.",
"So don't start over with another wave of guilt and a bigger promise. Start over smaller, clearer, and kinder. Trade one vague vow for a single measurable action at a specific time—and let this be the attempt that finally holds, because it was finally built to."
], "prayer": [
"Father, I'm tired of starting over, and tired of the shame that shows up with every restart. You know exactly how many times I've made this promise. I'm making it again—this time leaning on Your strength instead of just my own.",
"Thank You that Your mercy is new this morning: not a supply I've already exhausted, but grace freshly given, no matter how badly yesterday went. Help me receive it instead of trying to earn it.",
"Save me from vague vows and from self-punishment. Give me one clear, measurable step, and the humility to keep it small enough that I can actually keep it. Build the structure that holds me when the motivation is gone.",
"Teach me that circling back to the same lesson isn't failure—it's how You grow a man. Meet me in the spiral and keep me climbing instead of quitting.",
"Let my private follow-through and my public words finally start telling the same story. Make me a man who does what he says, beginning with today.",
"Your mercies are new. So am I. Amen."
]},
"9": {"teaching": [
"There's a specific weight a man carries when he feels he has disappointed the people who counted on him—a wife, a kid, a team, a friend. It isn't just guilt over one thing. It's the low, constant hum underneath everything that says you are, at your core, a letdown. That hum can quietly run a man into the ground.",
"Some of that weight is worth listening to. If you've genuinely dropped something that mattered, the honest move is not to spin it or bury it, but to own it cleanly—no over-explaining, no sliding the blame into someone else's lap. I was wrong, and here's what I'm going to do about it is one of the strongest sentences a man can learn to say.",
"But some of that weight is a lie. Feeling like you've let everyone down is not the same as actually having done so. Disappointment is often just the tax on being someone people depend on. You cannot meet every expectation, and you were never meant to be God, no matter how hard you've tried to play the role.",
"David didn't ask God to fix his reputation. He asked for a clean heart and a steady spirit—a renewed interior, not a repaired image. That's the deeper repair. God is far more interested in restoring the man than in rescuing the highlight reel other people see.",
"So make the one apology you keep avoiding. Take the one corrective action you keep postponing. Then let God do what shame never could—give you a clean heart and let you move forward as a forgiven man, not a failed one."
], "prayer": [
"God, I feel like I've let down the people who count on me, and the weight of it is heavy. Some of that is true and some of it is a lie. Help me tell the difference honestly, because You don't turn away from a man who comes to You real.",
"Where I've genuinely fallen short, give me the courage to own it cleanly—no excuses, no shifting the blame—and to make the apology or the repair I've been avoiding.",
"Where I've simply carried more than any man could, free me from the impossible job of never disappointing anyone. I was never meant to be everyone's god.",
"Like David, I'm not asking You to fix my reputation. Create in me a clean heart and renew a steady spirit within me. Restore the man, not just the image.",
"Let me walk forward as a forgiven man instead of a failed one—secure enough to try again and humble enough to keep growing.",
"Make my heart clean. Amen."
]},
"10": {"teaching": [
"A man can keep performing strength long after the inside has started to give way. He hits his deadlines. He holds the door. He says good, you? on autopilot. And all the while something essential is quietly deteriorating, because he decided a long time ago that admitting he wasn't okay was not an option a real man had available to him.",
"That belief is a slow leak on the soul. The refusal to admit weakness doesn't make you strong; it just leaves you alone with it. And what you won't say out loud tends to grow in the dark—the exhaustion, the temptation, the low-grade despair you keep promising yourself you'll deal with tomorrow.",
"God turns the entire equation upside down. He told Paul that His grace was enough, and that His power shows up most clearly right where a man admits he is weak. Not where you fake competence—where you tell the truth about your limits. That honesty is the doorway His strength actually walks through.",
"So the strongest thing you may do all week is say five honest words to someone safe: I am not doing well. Not a speech. Not a full diagnosis. Just the truth, followed by one concrete request for help. Wisdom is knowing the difference between what you're meant to carry and what you're meant to hand off.",
"You are not the exception who has to hold it all together alone. Admitting you're not okay is not the collapse of your strength. It's the beginning of the kind of strength that actually lasts."
], "prayer": [
"Lord, I've been performing strength while things quietly come apart inside. You see what the mask is hiding. I'm setting it down in front of You right now, because I cannot keep holding it up much longer.",
"I confess I've believed that admitting weakness makes me less of a man. Teach me Your upside-down truth—that Your power shows up most clearly in the exact place I stop pretending.",
"Your grace is enough for me. Not my competence, not my performance—Your grace. Let it meet me in the place I've been too proud or too afraid to admit even exists.",
"Give me the courage to say the honest words to someone safe: I am not doing well. And give me the humility to ask for the specific help I actually need.",
"Show me the difference between what I'm meant to carry and what I'm meant to hand off. I don't want to be strong and alone. I want to be honest and held.",
"Your grace is enough. Amen."
]},
"11": {"teaching": [
"Grief keeps a different clock than the world around it. The funeral ends, the messages taper off, everyone returns to normal—and you're still standing in the crater, expected to function as though the ground didn't move under you. So you carry it privately, stacked on top of everything else, and tell no one how heavy it still is.",
"Somewhere a man was taught that grief comes with a deadline, and that mourning too long is a kind of weakness. It isn't. Loss changes you, and real change takes time the calendar refuses to respect. Rushing grief doesn't heal it; it just buries it alive, where it keeps shaping you from underneath, unseen.",
"If you ever doubt whether God takes your sorrow seriously, remember the shortest verse in the Bible: Jesus wept. He stood at a grave He was about to open and still let the tears come. God does not stand at a cool distance from your grief, arms folded, waiting for you to pull it together. He steps into it with you.",
"Endurance in grief is not about staying productive through the pain. Sometimes the strongest, most faithful thing a man can do is stop—give himself twenty uninterrupted minutes to remember, to write, to cry, to pray, or just to sit quietly and let it be as heavy as it honestly is.",
"You don't have to carry this alone, and you don't have to carry it fast. Let God grieve it alongside you, and let one trusted person in. Sorrow shared is still sorrow—but it finally stops being solitary."
], "prayer": [
"God, I'm still carrying a loss the rest of the world has already moved past. The grief is quieter now, but it hasn't gone, and I've been holding most of it alone. I bring it to You tonight.",
"Thank You that You are not distant from my sorrow. You wept at a grave. You know grief from the inside, and You don't rush me or shame me for still hurting the way I do.",
"Give me permission to actually mourn—to stop, to remember, to cry if I need to—without labeling it weakness or trying to stay productive through the ache.",
"Hold the part of me that got buried under everything I had to keep doing. Grieve this with me, and bring the slow healing that only unhurried time with You can bring.",
"And give me the courage to let one trusted person in, so I stop carrying this in complete silence.",
"Stay close to my breaking heart. Amen."
]},
"12": {"teaching": [
"Self-sufficiency has great branding. We treat I don't need anything from anyone as a virtue, a badge for the man who's got it handled. But strip the marketing off, and it's often just fear wearing a strong face—the fear that if people saw your need up close, they'd decide you were a burden and quietly back away.",
"That fear runs a lot of men's lives. You'd help a friend in a heartbeat and never once think less of him for asking. But when it's your turn, you go silent, downplay it, insist you're fine—applying a standard to yourself you would never dream of applying to anyone you love.",
"The Bible treats interdependence as design, not defect. Two are better than one, it says, because when one of them falls, the other can lift him back up. That line assumes you'll fall sometimes, and that being lifted is exactly what the other man is for. Needing help isn't a flaw in the system. It is the system.",
"Asking well is a skill, and it's simpler than you fear. You don't have to unload your whole life on anyone. You just trade I'm fine for one specific request: could you help me with this? Specific is easier to say and easier to answer—and it hands the other man the quiet gift of being useful to you.",
"Let someone in. The people who love you are not keeping a tally of your needs the way you are. And the humility to receive help is the very same humility that keeps a man teachable, honest, and whole. The strongest men I know are the ones secure enough to need someone."
], "prayer": [
"Father, I've believed that needing help makes me a burden, so I've gone silent and called it strength. You see the fear underneath the self-sufficiency. I'm bringing it into the open with You instead of managing it alone.",
"Forgive me for the pride that insists I handle everything by myself. Give me the same grace toward my own need that I'd freely hand any friend who asked me for help.",
"Thank You that You designed me for others—that two really are better than one, and that being lifted when I fall is not weakness but Your good design doing exactly what it was made to do.",
"Give me the humility to ask for one specific thing this week instead of hiding behind I'm fine. And give me the courage to trust that the right people won't back away.",
"Keep me teachable and honest. Let me offer help freely and receive it without shame.",
"Teach me to lean, and to trust. Amen."
]},
}
path="rewrites.json"
data=json.load(open(path)) if os.path.exists(path) else {}
data.update(B)
json.dump(data, open(path,"w"), ensure_ascii=False, indent=1)
print("merged batch 1; rewrites now has", len(data), "devotions")
