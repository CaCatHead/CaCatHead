export const DefaultCheckers = [
  {
    name: `fcmp`,
    comment: `Lines, doesn't ignore whitespaces`,
    language: 'cpp',
    code: `#include "testlib.h"
#include <string>

using namespace std;

int main(int argc, char *argv[]) {
    setName("compare files as sequence of lines");
    registerTestlibCmd(argc, argv);

    std::string strAnswer;

    int n = 0;
    while (!ans.eof()) {
        std::string j = ans.readString();

        if (j.empty() && ans.eof())
            break;

        strAnswer = j;
        std::string p = ouf.readString();

        n++;

        if (j != p)
            quitf(_wa, "%d%s lines differ - expected: '%s', found: '%s'", n, englishEnding(n).c_str(),
                  compress(j).c_str(), compress(p).c_str());
    }

    if (n == 1)
        quitf(_ok, "single line: '%s'", compress(strAnswer).c_str());

    quitf(_ok, "%d lines", n);
}`,
  },
  {
    name: `hcmp`,
    comment: `Single huge integer`,
    language: 'cpp',
    code: `#include "testlib.h"
#include <string>

using namespace std;

pattern pnum("0|-?[1-9][0-9]*");

bool isNumeric(const string &p) {
    return pnum.matches(p);
}

int main(int argc, char *argv[]) {
    setName("compare two signed huge integers");
    registerTestlibCmd(argc, argv);

    string ja = ans.readWord();
    string pa = ouf.readWord();

    if (!isNumeric(ja))
        quitf(_fail, "%s is not a valid integer", compress(ja).c_str());

    if (!ans.seekEof())
        quitf(_fail, "expected exactly one token in the answer file");

    if (!isNumeric(pa))
        quitf(_pe, "%s is not a valid integer", compress(pa).c_str());

    if (ja != pa)
        quitf(_wa, "expected '%s', found '%s'", compress(ja).c_str(), compress(pa).c_str());

    quitf(_ok, "answer is '%s'", compress(ja).c_str());
}`,
  },
  {
    name: 'lcmp',
    comment: `Lines, ignores whitespaces`,
    language: 'cpp',
    code: `#include "testlib.h"
#include <string>
#include <vector>
#include <sstream>
  
using namespace std;
  
bool compareWords(string a, string b)
{
    vector<string> va, vb;
    stringstream sa;
    
    sa << a;
    string cur;
    while (sa >> cur)
        va.push_back(cur);
  
    stringstream sb;
    sb << b;
    while (sb >> cur)
        vb.push_back(cur);
  
    return (va == vb);
}
  
int main(int argc, char * argv[])
{
    setName("compare files as sequence of tokens in lines");
    registerTestlibCmd(argc, argv);
  
    std::string strAnswer;
  
    int n = 0;
    while (!ans.eof()) 
    {
        std::string j = ans.readString();
  
        if (j == "" && ans.eof())
          break;
        
        std::string p = ouf.readString();
        strAnswer = p;
  
        n++;
  
        if (!compareWords(j, p))
            quitf(_wa, "%d%s lines differ - expected: '%s', found: '%s'", n, englishEnding(n).c_str(), compress(j).c_str(), compress(p).c_str());
    }
    
    if (n == 1)
        quitf(_ok, "single line: '%s'", compress(strAnswer).c_str());
    
    quitf(_ok, "%d lines", n);
}`,
  },
  {
    name: `ncmp`,
    comment: `Single or more int64, ignores whitespaces`,
    language: 'cpp',
    code: `#include "testlib.h"

using namespace std;

int main(int argc, char *argv[]) {
    setName("compare ordered sequences of signed int%d numbers", 8 * int(sizeof(long long)));

    registerTestlibCmd(argc, argv);

    int n = 0;
    string firstElems;

    while (!ans.seekEof() && !ouf.seekEof()) {
        n++;
        long long j = ans.readLong();
        long long p = ouf.readLong();
        if (j != p)
            quitf(_wa, "%d%s numbers differ - expected: '%s', found: '%s'", n, englishEnding(n).c_str(),
                  vtos(j).c_str(), vtos(p).c_str());
        else if (n <= 5) {
            if (firstElems.length() > 0)
                firstElems += " ";
            firstElems += vtos(j);
        }
    }

    int extraInAnsCount = 0;

    while (!ans.seekEof()) {
        ans.readLong();
        extraInAnsCount++;
    }

    int extraInOufCount = 0;

    while (!ouf.seekEof()) {
        ouf.readLong();
        extraInOufCount++;
    }

    if (extraInAnsCount > 0)
        quitf(_wa, "Answer contains longer sequence [length = %d], but output contains %d elements",
              n + extraInAnsCount, n);

    if (extraInOufCount > 0)
        quitf(_wa, "Output contains longer sequence [length = %d], but answer contains %d elements",
              n + extraInOufCount, n);

    if (n <= 5)
        quitf(_ok, "%d number(s): \"%s\"", n, compress(firstElems).c_str());
    else
        quitf(_ok, "%d numbers", n);
}`,
  },
  {
    name: `nyesno`,
    comment: `Zero or more yes/no, case insensetive`,
    language: 'cpp',
    code: `#include "testlib.h"
#include <string>

using namespace std;

const string YES = "YES";
const string NO = "NO";

int main(int argc, char *argv[]) {
    setName("%s", ("multiple " + YES + "/" + NO + " (case insensetive)").c_str());
    registerTestlibCmd(argc, argv);

    int index = 0, yesCount = 0, noCount = 0;
    string pa;
    while (!ans.seekEof() && !ouf.seekEof()) {
        index++;
        string ja = upperCase(ans.readToken());
        pa = upperCase(ouf.readToken());

        if (ja != YES && ja != NO)
            quitf(_fail, "%s or %s expected in answer, but %s found [%d%s token]",
                  YES.c_str(), NO.c_str(), compress(ja).c_str(), index, englishEnding(index).c_str());

        if (pa == YES)
            yesCount++;
        else if (pa == NO)
            noCount++;
        else
            quitf(_pe, "%s or %s expected, but %s found [%d%s token]",
                  YES.c_str(), NO.c_str(), compress(pa).c_str(), index, englishEnding(index).c_str());

        if (ja != pa)
            quitf(_wa, "expected %s, found %s [%d%s token]",
                  compress(ja).c_str(), compress(pa).c_str(), index, englishEnding(index).c_str());
    }

    int extraInAnsCount = 0;
    while (!ans.seekEof()) {
        ans.readToken();
        extraInAnsCount++;
    }

    int extraInOufCount = 0;
    while (!ouf.seekEof()) {
        ouf.readToken();
        extraInOufCount++;
    }

    if (extraInAnsCount > 0)
        quitf(_wa, "Answer contains longer sequence [length = %d], but output contains %d elements",
              index + extraInAnsCount, index);

    if (extraInOufCount > 0)
        quitf(_wa, "Output contains longer sequence [length = %d], but answer contains %d elements",
              index + extraInOufCount, index);

    if (index == 0)
        quitf(_ok, "Empty output");
    else if (index == 1)
        quitf(_ok, "%s", pa.c_str());
    else
        quitf(_ok, "%d token(s): yes count is %d, no count is %d", index, yesCount, noCount);

    quitf(_fail, "Impossible case");
}`,
  },
  {
    name: `rcmp4`,
    comment: `Single or more double, max any error 1E-4`,
    language: 'cpp',
    code: `#include "testlib.h"

using namespace std;

const double EPS = 1E-4;

int main(int argc, char *argv[]) {
    setName("compare two sequences of doubles, max absolute or relative error = %.5f", EPS);
    registerTestlibCmd(argc, argv);

    int n = 0;
    double j = 0, p = 0;

    while (!ans.seekEof()) {
        n++;
        j = ans.readDouble();
        p = ouf.readDouble();
        if (!doubleCompare(j, p, EPS)) {
            quitf(_wa, "%d%s numbers differ - expected: '%.5f', found: '%.5f', error = '%.5f'",
                  n, englishEnding(n).c_str(), j, p, doubleDelta(j, p));
        }
    }

    if (n == 1)
        quitf(_ok, "found '%.5f', expected '%.5f', error '%.5f'", p, j, doubleDelta(j, p));

    quitf(_ok, "%d numbers", n);
}`,
  },
  {
    name: `rcmp6`,
    comment: `Single or more double, max any error 1E-6`,
    language: 'cpp',
    code: `#include "testlib.h"

using namespace std;

const double EPS = 1E-6;

int main(int argc, char *argv[]) {
    setName("compare two sequences of doubles, max absolute or relative  error = %.7f", EPS);
    registerTestlibCmd(argc, argv);

    int n = 0;
    double j = 0, p = 0;

    while (!ans.seekEof()) {
        n++;
        j = ans.readDouble();
        p = ouf.readDouble();
        if (!doubleCompare(j, p, EPS)) {
            quitf(_wa, "%d%s numbers differ - expected: '%.7f', found: '%.7f', error = '%.7f'",
                  n, englishEnding(n).c_str(), j, p, doubleDelta(j, p));
        }
    }

    if (n == 1)
        quitf(_ok, "found '%.7f', expected '%.7f', error '%.7f'", p, j, doubleDelta(j, p));

    quitf(_ok, "%d numbers", n);
}`,
  },
  {
    name: `rcmp9`,
    comment: `Single or more double, max any error 1E-9`,
    language: 'cpp',
    code: `#include "testlib.h"

using namespace std;

const double EPS = 1E-9;

int main(int argc, char *argv[]) {
    setName("compare two sequences of doubles, max absolute or relative error = %.10f", EPS);
    registerTestlibCmd(argc, argv);

    int n = 0;
    double j = 0, p = 0;

    while (!ans.seekEof()) {
        n++;
        j = ans.readDouble();
        p = ouf.readDouble();
        if (!doubleCompare(j, p, EPS)) {
            quitf(_wa, "%d%s numbers differ - expected: '%.10f', found: '%.10f', error = '%.10f'",
                  n, englishEnding(n).c_str(), j, p, doubleDelta(j, p));
        }
    }

    if (n == 1)
        quitf(_ok, "found '%.10f', expected '%.10f', error '%.10f'", p, j, doubleDelta(j, p));

    quitf(_ok, "%d numbers", n);
}`,
  },
  {
    name: `wcmp`,
    comment: `Sequence of tokens`,
    language: 'cpp',
    code: `#include "testlib.h"

using namespace std;

int main(int argc, char *argv[]) {
    setName("compare sequences of tokens");
    registerTestlibCmd(argc, argv);

    int n = 0;
    string j, p;

    while (!ans.seekEof() && !ouf.seekEof()) {
        n++;

        ans.readWordTo(j);
        ouf.readWordTo(p);

        if (j != p)
            quitf(_wa, "%d%s words differ - expected: '%s', found: '%s'", n, englishEnding(n).c_str(),
                  compress(j).c_str(), compress(p).c_str());
    }

    if (ans.seekEof() && ouf.seekEof()) {
        if (n == 1)
            quitf(_ok, "\"%s\"", compress(j).c_str());
        else
            quitf(_ok, "%d tokens", n);
    } else {
        if (ans.seekEof())
            quitf(_wa, "Participant output contains extra tokens");
        else
            quitf(_wa, "Unexpected EOF in the participants output");
    }
}`,
  },
  {
    name: `yesno`,
    comment: `Single yes or no, case insensetive`,
    language: 'cpp',
    code: `#include "testlib.h"
#include <string>

using namespace std;

const string YES = "YES";
const string NO = "NO";

int main(int argc, char *argv[]) {
    setName("%s", (YES + " or " + NO + " (case insensitive)").c_str());
    registerTestlibCmd(argc, argv);

    std::string ja = upperCase(ans.readWord());
    std::string pa = upperCase(ouf.readWord());

    if (ja != YES && ja != NO)
        quitf(_fail, "%s or %s expected in answer, but %s found", YES.c_str(), NO.c_str(), compress(ja).c_str());

    if (pa != YES && pa != NO)
        quitf(_pe, "%s or %s expected, but %s found", YES.c_str(), NO.c_str(), compress(pa).c_str());

    if (ja != pa)
        quitf(_wa, "expected %s, found %s", compress(ja).c_str(), compress(pa).c_str());

    quitf(_ok, "answer is %s", ja.c_str());
}`,
  },
];
