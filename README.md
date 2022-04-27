# Furniture-Ecommerce
 Furniture buying and selling website
 
I. Giới thiệu
1. Giới thiệu chung về website
	Hurst là một website thương mại điện tử, nơi mà người dùng có thể mua/bán các sản phẩm về đồ nội thất. Người dùng chỉ cần đăng ký một tài khoản trên website, lựa chọn các sản phẩm ưng ý cho ngôi nhà của mình. Hoặc tạo một cửa hàng riêng mới và bắt đầu việc kinh doanh 

2. Công nghệ sử dụng
	Front-end: html, css, java-script
	Back-end: Flask-Python
	Database: SqlAlchemy-Python

3. Thiết kế hệ thống và cơ sở dữ liệu

	Thiết kế hệ thống
	
	Thiết kế cơ sở dữ liệu

4. Ưu, nhược điểm và phương hướng phát triển trong tương lai

a) Ưu điểm
- Các tính năng có giao diện đơn giản, dễ hiểu cho người dùng
- Có đầy đủ chức năng cơ bản của 1 website thương mại điện tử 
- Hệ thống phù hợp cho mọi đối tượng người mua và người bán 
b) Nhược điểm
- Hệ thống chưa có những giải pháp tối ưu về hiệu suất
- Phương pháp tìm kiếm, sắp xếp theo yêu cầu người dùng chưa tối ưu
- Phương thức thanh toán chưa đa dạng 
c) Phương hướng phát triển
- Tối ưu hiệu suất cho hệ thống, đảm bảo hệ thống hoạt động với lưu lượng người dùng lớn 
- Thêm các phương thức thanh toán online, ví điện tử,...
- Thêm tính năng trò chuyện (chat) giữa người mua và người bán
- Thêm chức năng so sánh, hiển thị sản phẩm tương tự, đưa ra gợi ý cho người dùng dựa vào lịch sử xem hàng 
II. Chi tiết các tính năng 
1. Đăng ký / Đăng nhập
- Mô tả: Người dùng đăng ký/ đăng nhập tài khoản người dùng để truy cập vào website. Tên đăng nhập là duy nhất, mật khẩu được lưu dưới dạng hashcode sha. Sau khi sở hữu tài khoản, người dùng có thể tự sửa đổi mật khẩu, thông tin cá nhân của mình

2. Xem thông tin chi tiết người dùng, cửa hàng, sản phẩm
- Mô tả:
+ Người dùng click vào tên hiển thị của người dùng khác để xem thông tin cá nhân công khai của họ
+ Người dùng chọn vào cửa hàng để xem thông tin, danh sách sản phẩm của cửa hàng đó
+ Người dùng chọn vào sản phẩm để xem chi tiết thông tin về sản phẩm

3. Tạo cửa hàng cá nhân
- Mô tả: Nếu người dùng chưa có cửa hàng, người dùng có thể tạo 1 cửa hàng cá nhân của riêng mình. Mỗi tài khoản chỉ có thể tạo 1 cửa hàng cá nhân

4. Thêm một sản phẩm mới cho cửa hàng
Mô tả: Người dùng thêm mới 1 sản phẩm cho cửa hàng của mình quản lý 

5. Chỉnh sửa sản phẩm, cửa hàng
- Mô tả: Người dùng thay đổi, chỉnh sửa thông tin về cửa hàng, sản phẩm, hoặc xóa sản phẩm ra khỏi cửa hàng

6. Người dùng mua hàng
- Mô tả: Người dùng chọn những sản phẩm ưng ý thêm vào giỏ hàng, tiến hành chọn hình thức thanh toán rồi theo dõi đơn hàng
+ Thêm vào giỏ hàng cá nhân
+ Thanh toán
+ Theo dõi, xác nhận, hủy đơn hàng

7. Người bán tiếp nhận đơn hàng
- Mô tả: Sau khi người dùng xác nhận mua hàng, thông báo và đơn hàng sẽ gửi về cho quản lý cửa hàng đó

8 Bình luận, review về sản phẩm
- Mô tả: Người dùng đăng tải bình luận, review của mình bên dưới mỗi sản phẩm 

9. Quyền Admin
- Mô tả: Tài khoản admin là tài khoản có quyền cao nhất: quản lý, sửa, xóa mọi đối tượng trên website. Được tạo đầu tiên cùng với database
+ user name: admin
+ password: admin 

10. Review 3D

a) Sử dụng file model 3D 
- Mô tả: Quản lý cửa hàng thêm các file model 3D cho các sản phẩm của mình. Người dùng xem sản phẩm có thể chọn xem dưới dạng 3D
Sử dụng thư viện Three.js (https://threejs.org )để hiển thị model lên trên website 

b) Tạo view 360 
- Mô tả: Quản lý cửa hàng thêm các ảnh tuần tự là các góc view của sản phẩm để tạo nên 1 view 360 6 chiều cho sản phẩm 

Chi tiết xem tại: https://docs.google.com/document/d/19kDhtxWAqllHD6LtUW6xt9ZfiWGUJy31KmeoQfQSYII/edit?usp=sharing

III. Triển khai
1. Cài đặt các thư viện của python: flask, flask_sqlalchemy, werkzeug.securit, werkzeug.utils, flask_login, sqlalchemy.sql,...
2. Run file main.py và truy cập vào localhost

