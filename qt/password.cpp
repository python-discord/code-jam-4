#include "password.h"
#include "ui_password.h"

password::password(QWidget *parent) :
    QWidget(parent),
    ui(new Ui::password)
{
    ui->setupUi(this);
}

password::~password()
{
    delete ui;
}
