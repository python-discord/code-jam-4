#ifndef PASSWORD_H
#define PASSWORD_H

#include <QWidget>

namespace Ui {
class password;
}

class password : public QWidget
{
    Q_OBJECT

public:
    explicit password(QWidget *parent = nullptr);
    ~password();

private:
    Ui::password *ui;
};

#endif // PASSWORD_H
