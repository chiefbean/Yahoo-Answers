from bs4 import BeautifulSoup

def findQs(soup, cat):
    qs = soup.findAll("div", id=lambda x: x and x.startswith('qnaContainer'))
    if qs is None:
        return

    for qna in qs:
        question = {}
        question["user"] = qna.find("a", class_=lambda x: x and x.startswith("UserProfile__userName")).string
        question["title"] = qna.find("h1").string
        question["question"] = qna.select("div[class^=Question__content]")[0].string
        question["category"] = cat
        answers = []
        answerList = qna.select("ul[class^=AnswersList__answersList]")[0]
        for li in answerList.findAll("li"):
            try:
                answers.append({"user":li.find("a", class_=lambda x: x and x.startswith("UserProfile__userName")).string, "answer":li.find("p").string})
            except Exception:
                continue
        question["answers"] = answers
        print(cat + ": " + question["title"])
        return question

def convertHTML(html):
    return BeautifulSoup(html, 'html.parser')