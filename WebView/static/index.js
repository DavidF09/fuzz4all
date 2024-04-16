function updateView() 
{
    let bugSelect = document.getElementById("bugs");
    let bugs = bugSelect.options[bugSelect.selectedIndex].value;

    console.log(bugs);

    let bug_type = document.getElementById("bug_type");

    if (bugs == "clang")
    {
        bug_type.innerHTML = "Clang Bugs Data";

        document.getElementById("clang").style.display = "block";
        document.getElementById("cvc5").style.display = "none";
        document.getElementById("gcc").style.display = "none";
        document.getElementById("go").style.display = "none";
        document.getElementById("java").style.display = "none";
        document.getElementById("qiskit").style.display = "none";
        document.getElementById("z3").style.display = "none";
    }
    else if (bugs == "cvc5")
    {
        bug_type.innerHTML = "cvc5 Bugs Data";

        document.getElementById("clang").style.display = "none";
        document.getElementById("cvc5").style.display = "block";
        document.getElementById("gcc").style.display = "none";
        document.getElementById("go").style.display = "none";
        document.getElementById("java").style.display = "none";
        document.getElementById("qiskit").style.display = "none";
        document.getElementById("z3").style.display = "none";
    }
    else if (bugs == "gcc")
    {
        bug_type.innerHTML = "gcc Bugs Data";

        document.getElementById("clang").style.display = "none";
        document.getElementById("cvc5").style.display = "none";
        document.getElementById("gcc").style.display = "block";
        document.getElementById("go").style.display = "none";
        document.getElementById("java").style.display = "none";
        document.getElementById("qiskit").style.display = "none";
        document.getElementById("z3").style.display = "none";
    }
    else if (bugs == "go")
    {
        bug_type.innerHTML = "Go Bugs Data";

        document.getElementById("clang").style.display = "none";
        document.getElementById("cvc5").style.display = "none";
        document.getElementById("gcc").style.display = "none";
        document.getElementById("go").style.display = "block";
        document.getElementById("java").style.display = "none";
        document.getElementById("qiskit").style.display = "none";
        document.getElementById("z3").style.display = "none";
    }
    else if (bugs == "java")
    {
        bug_type.innerHTML = "Java Bugs Data";

        document.getElementById("clang").style.display = "none";
        document.getElementById("cvc5").style.display = "none";
        document.getElementById("gcc").style.display = "none";
        document.getElementById("go").style.display = "none";
        document.getElementById("java").style.display = "block";
        document.getElementById("qiskit").style.display = "none";
        document.getElementById("z3").style.display = "none";
    }
    else if (bugs == "qiskit")
    {
        bug_type.innerHTML = "Qiskit Bugs Data";

        document.getElementById("clang").style.display = "none";
        document.getElementById("cvc5").style.display = "none";
        document.getElementById("gcc").style.display = "none";
        document.getElementById("go").style.display = "none";
        document.getElementById("java").style.display = "none";
        document.getElementById("qiskit").style.display = "block";
        document.getElementById("z3").style.display = "none";
    }
    else if (bugs == "z3")
    {
        bug_type.innerHTML = "z3 Bugs Data";

        document.getElementById("clang").style.display = "none";
        document.getElementById("cvc5").style.display = "none";
        document.getElementById("gcc").style.display = "none";
        document.getElementById("go").style.display = "none";
        document.getElementById("java").style.display = "none";
        document.getElementById("qiskit").style.display = "none";
        document.getElementById("z3").style.display = "block";
    }
}