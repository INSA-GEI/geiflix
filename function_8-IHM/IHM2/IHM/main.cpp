#include <QApplication>
#include <QProcess>
#include <QPushButton>
#include "mafenetre.h"

//using namespace std;

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);

    mafenetre fenetre;
    fenetre.setWindowTitle("Graphical User Interface ---> YDP");
    fenetre.setStyleSheet("background-color:white;");
    fenetre.show();

    //QProcess *process = new QProcess();
    //QString exec = "gnome-terminal";
    //process->start(exec);



    //QProcess process;
    //process.execute("mkdir /home/fiabilite/PROJET/folder");

    return app.exec();
}
