# Q-Learning-With-PyGame
 1-) Giriş
	Pekiştirmeli öğrenme (reinforcement learning), öznelerin (agent) bir görevi en yüksek
	kazançla tamamlayabilmek için hangi eylemleri gerçekleştirmeleri gerektigi ile
	ilgilenen bir makine öğrenmesi tekniğidir. Bu tür öğrenme algoritmaların girdisi
	öznelerin görev yapacakları farklı durumlardan oluşan bir ortam S, yapabilecekleri
	eylemler A, ortamdaki durumuna göre yapabilecekleri eylemleri belirleyen prensipler, bir
	durumdan diğer duruma geçtiklerinde elde edecekleri kazançtır.
	Q-learning pekiştirmeli bir öğrenme algoritmasıdır. Ortam hakkında hiçbir şeyin
	bilinmediği durumlarda, Q-learning algoritması ortamı brute-force şeklinde, her
	ortam için olası tüm aksiyonları takip ederek, problem çözümü için en karlı yolu
	bulmaya çalışır. Q-learning algoritmasının girdileri kazanç matrisi olarak adlandırılan R
	matrisidir. Bu matrisin satır ve sütunları ortamları temsil etmekte, R[i][j] değeri ise i
	durumundan j durumuna geçtiğinde elde edilen anlık kazanç değeridir. Eğer i
	durumunda j durumuna bir geçiş yoksa R[i][j] değeri -1, geçis var ancak j durumu
	hedef durum değilse değeri 0, j hedef durum ise değeri kullanıcı tarafından belirlenen bir
	kazanç değeridir.
	Q-learning algoritmasının çıktısı ise öğrenmenin kalitesini gösteren Q matrisidir.
	Q-learning iteratif bir algoritmadır ve tüm değerleri başlangıçta 0 olan Q matrisi
	optimal değerlere yakınsadığı da sona erer. Algoritma her iterasyonda rastgele bir
	durumdan öğrenmeye baslar, A’ya göre durum değiştirir ve Q matrisini günceller.
	A’ya göre hedef duruma ulaşıldığında iterasyon sona erer. A’ya göre bir durumdan
	birden fazla duruma geçis olabilir. Boyle bir durumda, olası geçişler den biri rastgele
	seçilir. Eğer seçilen durum hedef duruma ulaştırmıyorsa, durum rastgele olacak durum
	olarak belirlenir. Hedef duruma ulaşılanakadar iterasyon devam eder. Q matrisi aşağıdaki formüle göre güncellenir:
	Q(durum, aksiyon) = R(durum, aksiyon)+γ×Max{Q(sonraki durumlar, tüm aksiyonlar)} γ
	ogrenme katsayısıdır ve 0 ile 1 arasında bir değer alır.
 2-) Proje	
	Burada robotun Q learning algoritması kullanarak engel sütunlarından kaçması ve beyaz alanlardan
	geçerek doğru yol alması gerekiyor. 
	Robotumuz kullanıcının istediği bir kareden başlayıp kırmızı kutulara çarpmadan bitiş kısmına en kısa(maliyetle) yoldan
	ulaşırsa başarılı sayılacaktır.
	Ajan, herhangi bir beyaz kareden başlayarak sağa, sola, aşağı, yukarı ve çapraz hareket edebilir. Atılan
	adımlar belirleyici olmalı ve engele çarpışmadıkça başarılı olur. Robot en son duvara geldiğinde robot
	sadece aşağı hareket ederek istenilen noktaya  gelecektir. Sonuç olarak robot başlangıç noktasından
	istenilen hedefe gelinceye kadar hiçbir engele çarpmadan ve en kısa yolu bularak ödülü alır.
	
	
	İndirim faktörü γ = 0.9, kırmızıya çarparsa -5 ödül puanı,yeşil bitiş noktasına +100, diğer geçişlere
	-1 ödül puanı olarak hesaplanacaktır.
	
	A) Verilen 50 * 50’lİk matriste her bir kullanıcı kendine özgü engel oluşturup,matristeki değerleri
	random olarak atayacaktır.Bu matris değerlerini engel.txt dosyasına yazdırılacak.Örnek gösterim
	(1,1,K).
	B) Grafiksel ara yüzde belirlenen yollar, engeller ve duvarlar gösterilecektir(15p).
	C) Kullanıcı tarafından bir grafiksel arayüz tasarlanacak, bu ara yüzde ajan başlangıç noktası, hedef
	noktası istenecektir.
	D) Herhangi bir başlangıç noktasından hedef noktaya ulaşıncaya kadar ajanın yaptığı
	kazançların/maliyetin(episode via cost) ve bölüm adım sayısının (episode via step) grafiği
	çizdirecek.
	E) Sonuç olarak ise başlangıç karesinden hedef kareye giden en kısa yol grafiksel ara yüzde
	gösterilerek yol planı grafik üzerinde çizdirilecek.. .
