<?php
/**
 * Simple PHP Email Form Class
 * Giúp VSCode nhận diện class và tránh báo lỗi undefined class.
 */

class PHP_Email_Form {

    public $to;
    public $from_name;
    public $from_email;
    public $subject;
    public $ajax = false;
    public $smtp = array();
    private $messages = array();

    public function add_message($content, $label = '', $newline = 1) {
        $this->messages[] = ($label ? "$label: " : '') . $content . str_repeat("\n", $newline);
    }

    public function send() {
        // Ghép nội dung mail
        $body = implode("", $this->messages);

        // Nếu dùng SMTP thì bạn tự thêm code xử lý SMTP sau
        if (!empty($this->smtp)) {
            // Ở đây mình để trống — bạn có thể tích hợp PHPMailer nếu muốn SMTP
        }

        // Gửi mail bằng PHP mail()
        $headers = "From: {$this->from_name} <{$this->from_email}>\r\n";
        return mail($this->to, $this->subject, $body, $headers);
    }
}
