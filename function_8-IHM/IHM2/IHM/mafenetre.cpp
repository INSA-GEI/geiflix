#include "mafenetre.h"
#include <thread>
#include <iostream>

using namespace std;
mafenetre::mafenetre() : QWidget()
{
    this->passage_a_1=0;
    setFixedSize(750, 550);


    // Construction du bouton
    m_bouton_AV = new QPushButton("", this);
    m_bouton_AR = new QPushButton("", this);
    m_bouton_D = new QPushButton("", this);
    m_bouton_G = new QPushButton("", this);
    m_bouton_AU = new QPushButton("", this);


    m_bouton_AVD = new QPushButton("", this);
    m_bouton_AVG = new QPushButton("", this);
    m_bouton_ARG = new QPushButton("", this);
    m_bouton_ARD = new QPushButton("", this);
    m_bouton_MANU = new QPushButton("", this);
    m_bouton_AUTO = new QPushButton("", this);

    produit1 = new QPushButton("Tomatoes", this);
    produit2 = new QPushButton("Snickers ", this);
    produit3 = new QPushButton("Beer", this);
    produit4 = new QPushButton("Wood planks", this);



    m_bouton_D->setIcon(QIcon("D.png"));
    m_bouton_D->setIconSize(QSize(85,50));

    m_bouton_G->setIcon(QIcon("G.png"));
    m_bouton_G->setIconSize(QSize(85,50));

    m_bouton_AV->setIcon(QIcon("H.png"));
    m_bouton_AV->setIconSize(QSize(50,85));

    m_bouton_AR->setIcon(QIcon("B.png"));
    m_bouton_AR->setIconSize(QSize(50,85));

    m_bouton_AVG->setIcon(QIcon("AG.png"));
    m_bouton_AVG->setIconSize(QSize(85,85));

    m_bouton_AVD->setIcon(QIcon("AD.png"));
    m_bouton_AVD->setIconSize(QSize(85,85));

    m_bouton_ARG->setIcon(QIcon("RG.png"));
    m_bouton_ARG->setIconSize(QSize(85,85));

    m_bouton_ARD->setIcon(QIcon("RD.png"));
    m_bouton_ARD->setIconSize(QSize(85,85));

    m_bouton_AU->setIcon(QIcon("AU.jpg"));
    m_bouton_AU->setIconSize(QSize(85,85));

    m_bouton_MANU->setIcon(QIcon("MANU.png"));
    m_bouton_MANU->setIconSize(QSize(45,45));

    m_bouton_AUTO->setIcon(QIcon("AUTO.png"));
    m_bouton_AUTO->setIconSize(QSize(45,45));




    m_bouton_AV->setFont(QFont("Comic Sans MS", 14));
    m_bouton_AV->setCursor(Qt::PointingHandCursor);
    m_bouton_AV->move(175, 140);

    m_bouton_AR->setFont(QFont("Comic Sans MS", 14));
    m_bouton_AR->setCursor(Qt::PointingHandCursor);
    m_bouton_AR->move(175, 330);

    m_bouton_D->setFont(QFont("Comic Sans MS", 14));
    m_bouton_D->setCursor(Qt::PointingHandCursor);
    m_bouton_D->move(280, 250);

    m_bouton_G->setFont(QFont("Comic Sans MS", 14));
    m_bouton_G->setCursor(Qt::PointingHandCursor);
    m_bouton_G->move(30, 250);


    m_bouton_AVD->setFont(QFont("Comic Sans MS", 14));
    m_bouton_AVD->setCursor(Qt::PointingHandCursor);
    m_bouton_AVD->move(280, 140);

    m_bouton_AVG->setFont(QFont("Comic Sans MS", 14));
    m_bouton_AVG->setCursor(Qt::PointingHandCursor);
    m_bouton_AVG->move(30, 140);

    m_bouton_ARG->setFont(QFont("Comic Sans MS", 14));
    m_bouton_ARG->setCursor(Qt::PointingHandCursor);
    m_bouton_ARG->move(30, 330);

    m_bouton_ARD->setFont(QFont("Comic Sans MS", 14));
    m_bouton_ARD->setCursor(Qt::PointingHandCursor);
    m_bouton_ARD->move(280, 330);

    m_bouton_MANU->setFont(QFont("Comic Sans MS", 14));
    m_bouton_MANU->setCursor(Qt::PointingHandCursor);
    m_bouton_MANU->move(30, 460);
    m_bouton_MANU->setCheckable(true);

    m_bouton_AUTO->setFont(QFont("Comic Sans MS", 14));
    m_bouton_AUTO->setCursor(Qt::PointingHandCursor);
    m_bouton_AUTO->move(95, 460);


    m_bouton_AU->setFont(QFont("Comic Sans MS", 14));
    m_bouton_AU->setCursor(Qt::PointingHandCursor);
    m_bouton_AU->move(280, 450);




    produit1->setFont(QFont("Comic Sans MS", 14));
    produit1->setCursor(Qt::PointingHandCursor);
    produit1->move(530, 230);

    produit2->setFont(QFont("Comic Sans MS", 14));
    produit2->setCursor(Qt::PointingHandCursor);
    produit2->move(530, 280);

    produit3->setFont(QFont("Comic Sans MS", 14));
    produit3->setCursor(Qt::PointingHandCursor);
    produit3->move(530, 330);

    produit4->setFont(QFont("Comic Sans MS", 14));
    produit4->setCursor(Qt::PointingHandCursor);
    produit4->move(530, 380);





    QObject::connect(m_bouton_AV, SIGNAL(clicked()), this, SLOT(envoimessRasPi_AV()));
    QObject::connect(m_bouton_AR, SIGNAL(clicked()), this, SLOT(envoimessRasPi_AR()));
    QObject::connect(m_bouton_D, SIGNAL(clicked()), this, SLOT(envoimessRasPi_D()));
    QObject::connect(m_bouton_G, SIGNAL(clicked()), this, SLOT(envoimessRasPi_G()));

    QObject::connect(m_bouton_AVD, SIGNAL(clicked()), this, SLOT(envoimessRasPi_AVD()));
    QObject::connect(m_bouton_AVG, SIGNAL(clicked()), this, SLOT(envoimessRasPi_AVG()));
    QObject::connect(m_bouton_ARG, SIGNAL(clicked()), this, SLOT(envoimessRasPi_ARG()));
    QObject::connect(m_bouton_ARD, SIGNAL(clicked()), this, SLOT(envoimessRasPi_ARD()));

    QObject::connect(m_bouton_AU, SIGNAL(clicked()), this, SLOT(envoimessRasPi_AU()));
    QObject::connect(m_bouton_MANU, SIGNAL(clicked()), this, SLOT(envoimessRasPi_MANU()));
    QObject::connect(m_bouton_AUTO, SIGNAL(clicked()), this, SLOT(envoimessRasPi_AUTO()));

    QObject::connect(produit1, SIGNAL(clicked()), this, SLOT(envoimessRasPi_produit1()));
    QObject::connect(produit2, SIGNAL(clicked()), this, SLOT(envoimessRasPi_produit2()));
    QObject::connect(produit3, SIGNAL(clicked()), this, SLOT(envoimessRasPi_produit3()));
    QObject::connect(produit4, SIGNAL(clicked()), this, SLOT(envoimessRasPi_produit4()));


    label1 = new QLabel("Cargate's GUI", this); //créé le Label
    label1->setStyleSheet("font: 25pt; font-weight: bold; color: red");
    label1->move(80,40);
    label1->show();

    label2 = new QLabel("YDP", this); //créé le Label
    label2->setStyleSheet("font: 25pt; font-weight: bold; color: red");
    label2->move(660,515);
    label2->show();

    label3 = new QLabel("Your choice :", this); //créé le Label
    label3->setStyleSheet("font: 25pt; font-weight: bold; color: red");
    label3->move(480,135);
    label3->show();

    label4 = new QLabel("2 clicks for \nmanual control", this); //créé le Label
    label4->setStyleSheet("font: 8pt; font-weight: bold; color: red;");
    label4->move(10,520);
    label4->show();

    label5 = new QLabel("Press MANU to disable \nthe emergency stop", this); //créé le Label
    label5->setStyleSheet("font: 8pt; font-weight: bold; color: red;");
    label5->move(380,480);
    label5->show();

}




void mafenetre::envoimessRasPi_AV()
{
    std::cout<<"Avant"<<endl;
    QString prog = "mosquitto_pub";
    QStringList arg;
    arg << "-h" << "192.168.0.82" << "-t" << "test/message" << "-m" << "avancer";
    m_process_AV->execute(prog, arg);
}

void mafenetre::envoimessRasPi_AR()
{
    std::cout<<"Arriere"<<endl;
    QString prog = "mosquitto_pub";
    QStringList arg;
    arg << "-h" << "192.168.0.82" << "-t" << "test/message" << "-m" << "reculer";
    m_process_AR->execute(prog, arg);
}

void mafenetre::envoimessRasPi_D()
{
    std::cout<<"Droite"<<endl;
    QString prog = "mosquitto_pub";
    QStringList arg;
    arg << "-h" << "192.168.0.82" << "-t" << "test/message" << "-m" << "droite";
    m_process_D->execute(prog, arg);
}

void mafenetre::envoimessRasPi_G()
{
    std::cout<<"Gauche"<<endl;
    QString prog = "mosquitto_pub";
    QStringList arg;
    arg << "-h" << "192.168.0.82" << "-t" << "test/message" << "-m" << "gauche";
    m_process_G->execute(prog, arg);
}

void mafenetre::envoimessRasPi_AVG()
{
    std::cout<<"Avant Gauche"<<endl;
    QString prog = "mosquitto_pub";
    QStringList arg;
    arg << "-h" << "192.168.0.82" << "-t" << "test/message" << "-m" << "avancer_gauche";
    m_process_AV->execute(prog, arg);
}

void mafenetre::envoimessRasPi_AVD()
{
    std::cout<<"Avant Droite"<<endl;
    QString prog = "mosquitto_pub";
    QStringList arg;
    arg << "-h" << "192.168.0.82" << "-t" << "test/message" << "-m" << "avancer_droite";
    m_process_AR->execute(prog, arg);
}

void mafenetre::envoimessRasPi_ARG()
{
    std::cout<<"Arriere Gauche"<<endl;
    QString prog = "mosquitto_pub";
    QStringList arg;
    arg << "-h" << "192.168.0.82" << "-t" << "test/message" << "-m" << "reculer_gauche";
    m_process_D->execute(prog, arg);
}

void mafenetre::envoimessRasPi_ARD()
{
    std::cout<<"Arriere Droite"<<endl;
    QString prog = "mosquitto_pub";
    QStringList arg;
    arg << "-h" << "192.168.0.82" << "-t" << "test/message" << "-m" << "reculer_droite";
    m_process_G->execute(prog, arg);
}

void mafenetre::envoimessRasPi_AU()
{
    std::cout<<"Arret Urgence"<<endl;
    QString prog = "mosquitto_pub";
    QStringList arg;
    arg << "-h" << "192.168.0.82" << "-t" << "test/message" << "-m" << "Arret_Urgence";
    m_process_AV->execute(prog, arg);
}

void mafenetre::envoimessRasPi_MANU()
{
    std::cout<<"MANU"<<endl;
    QString prog = "mosquitto_pub";
    QStringList arg;
    arg << "-h" << "192.168.0.82" << "-t" << "test/message" << "-m" << "MANU";
    m_process_MANU->execute(prog, arg);
    this->passage_a_1=0;
}

void mafenetre::envoimessRasPi_AUTO()
{
    std::thread Thread1([this](){

        this->passage_a_1=1;

        while(this->passage_a_1==1){
            std::cout<<"AUTO"<<endl;
            QString prog = "mosquitto_pub";
            QStringList arg;
            arg << "-h" << "192.168.0.82" << "-t" << "test/message" << "-m" << "AUTO";
            m_process_AUTO->execute(prog, arg);
        }

    });
    Thread1.detach();

}


void mafenetre::envoimessRasPi_produit1()
{
    QString prog = "mosquitto_pub";
    QStringList arg;
    arg << "-h" << "192.168.0.82" << "-t" << "test/message" << "-m" << "10";
    m_process_AUTO->execute(prog, arg);
}

void mafenetre::envoimessRasPi_produit2()
{
    QString prog = "mosquitto_pub";
    QStringList arg;
    arg << "-h" << "192.168.0.82" << "-t" << "test/message" << "-m" << "20";
    m_process_AUTO->execute(prog, arg);
}

void mafenetre::envoimessRasPi_produit3()
{
    QString prog = "mosquitto_pub";
    QStringList arg;
    arg << "-h" << "192.168.0.82" << "-t" << "test/message" << "-m" << "25";
    m_process_AUTO->execute(prog, arg);
}

void mafenetre::envoimessRasPi_produit4()
{
    QString prog = "mosquitto_pub";
    QStringList arg;
    arg << "-h" << "192.168.0.82" << "-t" << "test/message" << "-m" << "30";
    m_process_AUTO->execute(prog, arg);
}

