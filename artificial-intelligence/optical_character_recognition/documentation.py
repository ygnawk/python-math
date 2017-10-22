import ocr
from PIL import Image as image


im = image.open('sample/sample_9.png')

test = ocr.ocr(im, nail_size = 25, blur_fact = 90, tolerance = 31)
# test.document.show()

# test.document.lines[0].chars[-1].show()
# print(len(test.classifier.symb_list))
# print(sum(1 for line in test.document.lines for i in line))




code = test.spit_text()

# print(repr(code))






text = """I see that I hold a sanctuary in their hearts, and in the hearts of
their descendants, generations hence.  I see her, an old woman,
weeping for me on the anniversary of this day.  I see her and her
husband, their course done, lying side by side in their last earthly
bed, and I know that each was not more honoured and held sacred in
the other's soul, than I was in the souls of both.
"I see that child who lay upon her bosom and who bore my name, a man
winning his way up in that path of life which once was mine.  I see
him winning it so well, that my name is made illustrious there by the
light of his.  I see the blots I threw upon it, faded away.  I see
him, fore-most of just judges and honoured men, bringing a boy of my
name, with a forehead that I know and golden hair, to this place--
then fair to look upon, with not a trace of this day's disfigurement
--and I hear him tell the child my story, with a tender and a faltering
voice.
"""







text = """I see Barsad, and Cly, Defarge, The Vengeance, the Juryman, the
Judge, long ranks of the new oppressors who have risen on the
destruction of the old, perishing by this retributive instrument,
before it shall cease out of its present use.  I see a beautiful city
and a brilliant people rising from this abyss, and, in their struggles
to be truly free, in their triumphs and defeats, through long years
to come, I see the evil of this time and of the previous time of
which this is the natural birth, gradually making expiation for
itself and wearing out.

I see the lives for which I lay down my life, peaceful, useful,
prosperous and happy, in that England which I shall see no more.
I see Her with a child upon her bosom, who bears my name.  I see her
father, aged and bent, but otherwise restored, and faithful to all
men in his healing office, and at peace.  I see the good old man, so
long their friend, in ten years' time enriching them with all he has,
and passing tranquilly to his reward.
"""




text = """
It was the best of times, it was the worst of times,
it was the age of wisdom, it was the age of foolishness,
it was the epoch of belief, it was the epoch of incredulity,
it was the season of Light, it was the season of Darkness,
it was the spring of hope, it was the winter of despair,
we had everything before us, we had nothing before us,
we were all going direct to Heaven, we were all going direct
the other way--in short, the period was so far like the present
period, that some of its noisiest authorities insisted on its
being received, for good or for evil, in the superlative degree
of comparison only.
It was the best of times, it was the worst of times,
it was the age of wisdom, it was the age of foolishness,
it was the epoch of belief, it was the epoch of incredulity,
it was the season of Light, it was the season of Darkness,
it was the spring of hope, it was the winter of despair,
we had everything before us, we had nothing before us,
we were all going direct to Heaven, we were all going direct
the other way--in short, the period was so far like the present
period, that some of its noisiest authorities insisted on its
being received, for good or for evil, in the superlative degree
of comparison only.

"""

text = """
The messenger rode back at an easy trot, stopping pretty often at
ale-houses by the way to drink, but evincing a tendency to keep his
own counsel, and to keep his hat cocked over his eyes.  He had eyes
that assorted very well with that decoration, being of a surface
black, with no depth in the colour or form, and much too near
together--as if they were afraid of being found out in something,
singly, if they kept too far apart.  They had a sinister expression,
under an old cocked-hat like a three-cornered spittoon, and over a
great muffler for the chin and throat, which descended nearly to the
wearer's knees.  When he stopped for drink, he moved this muffler
with his left hand, only while he poured his liquor in with his
right; as soon as that was done, he muffled again.


"""
text = text.replace("\"", "\'\'")
text = text.replace("  ", " ")

def get_indices(text, letter):
	return [index 
				for index, alpha
				in enumerate(text)
				if letter == alpha]

def slicer(text, indices):
	return [text[i] for i in indices]


def majority(text):
	return max((text.count(letter), letter) for letter in text)[1]

def decode(text, code):
	print(len(text), len(code))
	# assert len(text) == len(code)
	code = "".join(code)
	new = list(code)
	letter_dict = {}
	for d in set(code):
		indices = get_indices(code, d)
		letters = slicer(text, indices)
		alpha = majority(letters)
		new = [letter if letter != d else alpha for letter in new]
	return "".join(new)

print(code)
code = [' ' + code ]
print(decode(text, code))


print(test.classifier.tolerance)
print(len(test.classifier.symb_list))
test.document.show()
