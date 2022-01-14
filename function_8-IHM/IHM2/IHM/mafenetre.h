#ifndef MAFENETRE_H
#define MAFENETRE_H

#include <QApplication>
#include <QWidget>
#include <QPushButton>
#include <QLabel>
#include <QProcess>
#include <QLCDNumber>
#include <QSlider>


class mafenetre : public QWidget
{
    Q_OBJECT

public:
    mafenetre();

public slots:
    void envoimessRasPi_AV(void);
    void envoimessRasPi_AR(void);
    void envoimessRasPi_D(void);
    void envoimessRasPi_G(void);

    void envoimessRasPi_AVG(void);
    void envoimessRasPi_AVD(void);
    void envoimessRasPi_ARG(void);
    void envoimessRasPi_ARD(void);

    void envoimessRasPi_AU(void);

    void envoimessRasPi_MANU(void);
    void envoimessRasPi_AUTO(void);

    void envoimessRasPi_produit1(void);
    void envoimessRasPi_produit2(void);
    void envoimessRasPi_produit3(void);
    void envoimessRasPi_produit4(void);



private :
    QPushButton *m_bouton_AV;
    QPushButton *m_bouton_AR;
    QPushButton *m_bouton_D;
    QPushButton *m_bouton_G;

    QPushButton *m_bouton_AVG;
    QPushButton *m_bouton_AVD;
    QPushButton *m_bouton_ARG;
    QPushButton *m_bouton_ARD;

    QPushButton *m_bouton_AU;
    QPushButton *m_bouton_MANU;
    QPushButton *m_bouton_AUTO;

    QPushButton *produit1;
    QPushButton *produit2;
    QPushButton *produit3;
    QPushButton *produit4;


    QLabel *label1;
    QLabel *label2;
    QLabel *label3;




    QProcess *m_process_AV;
    QProcess *m_process_AR;
    QProcess *m_process_D;
    QProcess *m_process_G;

    QProcess *m_process_AVD;
    QProcess *m_process_AVG;
    QProcess *m_process_ARD;
    QProcess *m_process_ARG;

    QProcess *m_process_AU;
    QProcess *m_process_MANU;
    QProcess *m_process_AUTO;

    QProcess *m_process_produit1;
    QProcess *m_process_produit2;
    QProcess *m_process_produit3;
    QProcess *m_process_produit4;


    //QSlider *m_slider;
};

#endif // MAFENETRE_H
