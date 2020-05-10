
def map_forward_backward_month(s="2020-01-09", method="backward"):
    def f(year_month):
        y, m = year_month.split("-")
        if m == "01":
            m = "12"
            y = str(int(y) - 1)
        else:
            m = str(int(m) - 1).zfill(2)
        return y + "-" + m
    md_dict = {
        "/2": "28",
        "01": "31",
        "02": "28",
        "03": "31",
        "04": "30",
        "05": "31",
        "06": "30",
        "07": "31",
        "08": "31",
        "09": "30",
        "10": "31",
        "11": "30",
        "12": "31"}
    if method == "forward":
        return s[:8] + md_dict[s[5:7]]
    else:
        return f(s[:7]) + "-" + md_dict[f(s[:7])[5:]]


def rentree_func(date):
    if str(date) == "nan":
        return date

    if date.split("-")[1] in {"9", "10", "11", "12"}:
        return "Yes"
    else:
        return "No"

def freq_contact_func(x):
    if str(x) == "nan":
        return x
    if x <= 3:
        return str(x)
    else:
        return "4"


def contact_previous(x):
    if str(x) == "nan":
        return x
    if x == -1:
        return "Yes"
    else:
        return "No"